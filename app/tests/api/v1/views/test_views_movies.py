# test_movies.py
import pytest
from django.urls import reverse
from app.models import Movie, Rating


@pytest.mark.django_db
def test_movie_list_view(api_client, create_movie):
    create_movie(title="Movie 1", year=2020)
    create_movie(title="Movie 2", year=2021)

    url = reverse("movie-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_movie_create_view(api_client, user):
    api_client.force_authenticate(user=user)

    url = reverse("movie-list")
    new_movie_data = {
        "title": "New Movie",
        "year": 2022,
        "genres": "Drama, Comedy",
        "tags": "funny, dramatic",
    }
    response = api_client.post(url, new_movie_data)

    assert response.status_code == 201
    assert Movie.objects.count() == 1

    created_movie = Movie.objects.get()
    assert created_movie.title == "New Movie"
    assert created_movie.year == 2022


@pytest.mark.django_db
def test_movie_detail_view(api_client, create_movie):
    movie = create_movie(title="Movie 1", year=2020)

    url = reverse("movie-detail", args=[movie.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["title"] == "Movie 1"


@pytest.mark.django_db
def test_rate_movie_view(api_client, create_user, create_movie):
    user = create_user(username="user1", password="testpass123")
    movie = create_movie(title="Movie 1", year=2020)

    api_client.force_authenticate(user=user)

    url = reverse("movie-rate", args=[movie.id])
    response = api_client.post(url, {"rate": 5})

    assert response.status_code == 200
    assert Rating.objects.filter(user=user, movie=movie).exists()


@pytest.mark.django_db
def test_rate_movie_view_non_existent_movie(api_client, create_user):
    user = create_user(username="user2", password="testpass123")
    non_existent_movie_id = 999  # An ID that doesn't correspond to any movie

    api_client.force_authenticate(user=user)

    url = reverse("movie-rate", args=[non_existent_movie_id])
    response = api_client.post(url, {"rate": 5})

    assert response.status_code == 404
    assert "Movie not found" in response.data["error"]


@pytest.mark.django_db
def test_rate_movie_view_invalid_input(api_client, create_user, create_movie):
    user = create_user(username="user3", password="testpass123")
    movie = create_movie(title="Movie 2", year=2021)

    api_client.force_authenticate(user=user)

    url = reverse("movie-rate", args=[movie.id])
    response = api_client.post(url, {"rate": "invalid"})

    assert response.status_code == 400
    assert "rate" in response.data  # Assuming 'rate' field has validation error


@pytest.mark.django_db
def test_rate_movie_view_duplicate_rating(api_client, create_user, create_movie):
    user = create_user(username="user4", password="testpass123")
    movie = create_movie(title="Movie 3", year=2022)

    api_client.force_authenticate(user=user)

    url = reverse("movie-rate", args=[movie.id])
    api_client.post(url, {"rate": 4})
    response = api_client.post(
        url, {"rate": 3}
    )  # Second attempt to rate the same movie

    assert response.status_code == 400
    assert "You have already rated this movie" in response.data["error"]
