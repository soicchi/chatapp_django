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

    with pytest.raises(ValidationError, match="パスワードは255文字以内で入力してください"):
        over_length_password = "a" * 256
        serializer.validate_password(over_length_password)


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
def test_signup_validate_name():
    serializer = SignUpSerializer()
    valid_name = "testuser"
    assert serializer.validate_name(valid_name) == valid_name

    with pytest.raises(ValidationError, match="ユーザー名が空です"):
        serializer.validate_name("")

    with pytest.raises(ValidationError, match="ユーザー名は255文字以内で入力してください"):
        over_length_name = "a" * 256
        serializer.validate_name(over_length_name)


@pytest.mark.django_db
def test_signup_validate_email():
    serializer = SignUpSerializer()
    valid_email = "test@test.com"
    assert serializer.validate_email(valid_email) == valid_email

    with pytest.raises(ValidationError, match="メールアドレスが空です"):
        serializer.validate_email("")

    with pytest.raises(ValidationError, match="メールアドレスは255文字以内で入力してください"):
        over_length_email = "a" * 243 + "test@test.com"
        serializer.validate_email(over_length_email)


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
