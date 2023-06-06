import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from accounts.serializers import SignUpSerializer, UserUpdateSerializer


too_long_name_error_message = "ユーザー名は255文字以内で入力してください"
blank_name_error_message = "ユーザー名が空です"
too_long_email_error_message = "メールアドレスは255文字以内で入力してください"
blank_email_error_message = "メールアドレスが空です"
too_short_password_error_message = "パスワードは8文字以上で入力してください"
too_long_password_error_message = "パスワードは255文字以内で入力してください"
blank_password_error_message = "パスワードが空です"


def test_signup_validate_password():
    serializer = SignUpSerializer()

    valid_password = "a" * 255
    assert serializer.validate_password(valid_password) == valid_password

    with pytest.raises(ValidationError, match=too_short_password_error_message):
        too_short_password = "a" * 7
        serializer.validate_password(too_short_password)

    with pytest.raises(ValidationError, match=too_long_password_error_message):
        too_long_password = "a" * 256
        serializer.validate_password(too_long_password)


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
    valid_name = "a" * 255
    assert serializer.validate_name(valid_name) == valid_name

    with pytest.raises(ValidationError, match=blank_name_error_message):
        serializer.validate_name("")

    with pytest.raises(ValidationError, match=too_long_name_error_message):
        too_long_name = "a" * 256
        serializer.validate_name(too_long_name)


@pytest.mark.django_db
def test_signup_validate_email():
    serializer = SignUpSerializer()

    # 255文字のメールアドレスを生成
    valid_email = "a" * 242 + "test@test.com"
    assert serializer.validate_email(valid_email) == valid_email

    with pytest.raises(ValidationError, match=blank_email_error_message):
        serializer.validate_email("")

    with pytest.raises(ValidationError, match=too_long_email_error_message):

        # 256文字のメールアドレスを生成
        too_long_email = "a" * 243 + "test@test.com"
        serializer.validate_email(too_long_email)


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


@pytest.mark.django_db
def test_update_user_validate_name():
    serializer = SignUpSerializer()
    valid_name = "a" * 255
    assert serializer.validate_name(valid_name) == valid_name

    with pytest.raises(ValidationError, match=blank_name_error_message):
        serializer.validate_name("")

    with pytest.raises(ValidationError, match=too_long_name_error_message):
        too_long_name = "a" * 256
        serializer.validate_name(too_long_name)


@pytest.mark.django_db
def test_update_user_validate_email():
    serializer = SignUpSerializer()

    # 255文字のメールアドレスを生成
    valid_email = "a" * 242 + "test@test.com"
    assert serializer.validate_email(valid_email) == valid_email

    with pytest.raises(ValidationError, match=blank_email_error_message):
        serializer.validate_email("")

    with pytest.raises(ValidationError, match=too_long_email_error_message):

        # 256文字のメールアドレスを生成
        too_long_email = "a" * 243 + "test@test.com"
        serializer.validate_email(too_long_email)
