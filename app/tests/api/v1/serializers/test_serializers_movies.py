import pytest
from datetime import datetime

from app.api.v1.serializers.movies import (
    MovieSerializer,
    MovieCreateSerializer,
    RateSerializer,
    RatingSerializer,
)


@pytest.mark.django_db
def test_movie_serializer(movie):
    serializer = MovieSerializer(movie)
    assert serializer.data == {
        "id": movie.id,
        "title": "Inception",
        "year": 2010,
        "rate": movie.rate,
        "genres": "Action, Sci-Fi",
        "tags": movie.tags,
        "imdb_url": movie.imdb_url(),
        "tmdb_url": movie.tmdb_url(),
    }


@pytest.mark.django_db
def test_movie_create_serializer():
    movie_data = {
        "title": "New Movie",
        "year": 2021,
        "genres": "Drama",
        "tags": "inspiring",
        "imdb_id": "1234567",
        "tmdb_id": "7654321",
    }
    serializer = MovieCreateSerializer(data=movie_data)
    assert serializer.is_valid()
    created_movie = serializer.save()
    assert created_movie.title == "New Movie"


def test_rate_serializer():
    rate_data = {"rate": 9.5}
    serializer = RateSerializer(data=rate_data)
    assert serializer.is_valid()
    assert serializer.validated_data == rate_data


@pytest.mark.django_db
def test_rating_serializer(user, movie, rating):
    serializer = RatingSerializer(rating)
    data = serializer.data

    assert data["user"] == user.id
    assert data["movie"] == movie.id
    assert data["rate"] == 8.0
    # Validate that timestamp exists and is in the correct format
    assert "timestamp" in data
    try:
        datetime.fromisoformat(
            data["timestamp"]
        )  # This will raise an error if the format is incorrect
    except ValueError:
        pytest.fail("Timestamp is not in a valid ISO format")
