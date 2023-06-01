import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from accounts.serializers import SignUpSerializer


def test_validate_password():
    serializer = SignUpSerializer()

    valid_password = "password"
    assert serializer.validate_password(valid_password) == valid_password

    with pytest.raises(ValidationError, match="パスワードは8文字以上で入力してください"):
        serializer.validate_password("1234567")


@pytest.mark.django_db
def test_signup_serializer():
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "passwordtest",
    }

    # シリアライザのバリデーションチェック
    serializer = SignUpSerializer(data=input_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_signup_with_blank_name():
    input_data = {
        "name": "",
        "email": "test@test.com",
        "password": "passwordtest",
    }

    serializer = SignUpSerializer(data=input_data)
    with pytest.raises(ValidationError, match="ユーザー名が空です"):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_signup_with_over_length_name():
    over_length_name = "a" * 256
    input_data = {
        "name": over_length_name,
        "email": "test@test.com",
        "password": "passwordtest",
    }

    serializer = SignUpSerializer(data=input_data)
    with pytest.raises(ValidationError, match="ユーザー名は255文字以内で入力してください"):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_signup_with_blank_email():
    input_data = {
        "name": "testuser",
        "email": "",
        "password": "passwordtest",
    }

    serializer = SignUpSerializer(data=input_data)
    with pytest.raises(ValidationError, match="メールアドレスが空です"):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_signup_with_over_length_email():
    over_length_email = "test@test.com" + "a" * 243
    input_data = {
        "name": "testuser",
        "email": over_length_email,
        "password": "passwordtest",
    }

    serializer = SignUpSerializer(data=input_data)
    with pytest.raises(ValidationError, match="メールアドレスは255文字以内で入力してください"):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_signup_with_blank_password():
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "",
    }

    serializer = SignUpSerializer(data=input_data)
    with pytest.raises(ValidationError, match="パスワードが空です"):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_signup_with_over_length_password():
    over_length_password = "a" * 256
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": over_length_password,
    }

    serializer = SignUpSerializer(data=input_data)
    with pytest.raises(ValidationError, match="パスワードは255文字以内で入力してください"):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_include_token_in_response():
    User = get_user_model()
    new_user = User.objects.create_user(
        name="testuser",
        email="test@test.com",
        password="passwordtest",
    )

    serializer = SignUpSerializer(instance=new_user)
    response = serializer.to_representation(new_user)
    assert "refresh_token" in response
    assert "access_token" in response
