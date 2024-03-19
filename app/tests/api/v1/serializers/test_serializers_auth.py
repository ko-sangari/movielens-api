import pytest

from app.api.v1.serializers.auth import UserLoginSerializer


def test_user_login_serializer_with_valid_data():
    serializer = UserLoginSerializer(data={"username": "user", "password": "pass"})

    # Check that serializer is valid
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_user_login_serializer_with_invalid_data():
    # Test with missing password
    serializer = UserLoginSerializer(data={"username": "user"})

    # Check that serializer is not valid
    assert not serializer.is_valid()
    assert "password" in serializer.errors  # Password field should have errors

    # Test with missing username
    serializer = UserLoginSerializer(data={"password": "pass"})

    # Check that serializer is not valid
    assert not serializer.is_valid()
    assert "username" in serializer.errors  # Username field should have errors
