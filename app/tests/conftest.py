import pytest

from rest_framework.test import APIClient
from django.contrib.auth.models import User

from app.models import Movie, Rating


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_movie(db):
    def make_movie(**kwargs):
        return Movie.objects.create(**kwargs)

    return make_movie


@pytest.fixture
def movie():
    return Movie.objects.create(title="Inception", year=2010, genres="Action, Sci-Fi")


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def rating(user, movie):
    return Rating.objects.create(user=user, movie=movie, rate=8.0)
