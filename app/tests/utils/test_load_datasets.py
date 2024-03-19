import pytest
import pandas as pd

from app.models import Movie
from app.utils.load_datasets import (
    process_movies,
    process_links,
    process_tags,
    transform_title,
)


@pytest.fixture
def mock_data():
    return pd.DataFrame(
        {
            "movieId": [1, 2, 3],
            "title": [
                '"Toy Story, The (1995)"',
                '"Another Movie (1999)"',
                "Invalid Title",
            ],
            "genres": ["Animation, Comedy", "Drama", None],
            "tag": ["action", None, "drama"],
            "imdbId": ["0114709", "0113497", None],
            "tmdbId": ["862", "8844", None],
        }
    )


@pytest.mark.parametrize(
    "title, expected",
    [
        ('"Toy Story, The (1995)"', ("The Toy Story", "1995")),
        ('"Another Movie (1999)"', ("Another Movie", "1999")),
        ("Invalid Title", ("Invalid Title", None)),
    ],
)
def test_transform_title(title, expected):
    assert transform_title(title) == expected


@pytest.mark.django_db
def test_process_movies(mock_data):
    process_movies(mock_data[["movieId", "title", "genres"]])
    assert Movie.objects.count() == 2
    assert Movie.objects.get(pk=1).title == "The Toy Story"


@pytest.mark.django_db
def test_process_tags(mock_data):
    Movie.objects.create(pk=1, title="Movie One")
    Movie.objects.create(pk=3, title="Movie Three")

    process_tags(mock_data[["movieId", "tag"]])
    movie_one = Movie.objects.get(pk=1)
    movie_three = Movie.objects.get(pk=3)
    assert movie_one.tags == "action"
    assert movie_three.tags == "drama"


@pytest.mark.django_db
def test_process_links(mock_data):
    Movie.objects.create(pk=1, title="Movie One")
    Movie.objects.create(pk=2, title="Movie Two")

    process_links(mock_data[["movieId", "imdbId", "tmdbId"]])
    movie_one = Movie.objects.get(pk=1)
    movie_two = Movie.objects.get(pk=2)
    assert movie_one.imdb_id == "0114709"
    assert movie_one.tmdb_id == "862"
    assert movie_two.imdb_id == "0113497"
    assert movie_two.tmdb_id == "8844"
