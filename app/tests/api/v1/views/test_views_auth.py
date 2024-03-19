import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse("auth:register-user")
    data = {"username": "testuser", "password": "password123"}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "token" in response.data


def test_user_login(api_client, create_user):
    user = create_user(username="testuser", password="password123")
    url = reverse("auth:login-user")
    data = {"username": "testuser", "password": "password123"}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "token" in response.data


def test_token_refresh(api_client, create_user):
    user = create_user(username="testuser", password="password123")
    url = reverse("auth:login-user")
    data = {"username": "testuser", "password": "password123"}
    response = api_client.post(url, data)
    refresh_token = response.data["refresh"]

    url = reverse("auth:token-refresh")
    data = {"refresh": refresh_token}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "access" in response.data
