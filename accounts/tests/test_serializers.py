import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from accounts.serializers import SignUpSerializer, UserUpdateSerializer

TOO_LONG_NAME_ERROR_MESSAGE = "ユーザー名は255文字以内で入力してください"
BLANK_NAME_ERROR_MESSAGE = "ユーザー名が空です"
TOO_LONG_EMAIL_ERROR_MESSAGE = "メールアドレスは255文字以内で入力してください"
BLANK_EMAIL_ERROR_MESSAGE = "メールアドレスが空です"
TOO_SHORT_PASSWORD_ERROR_MESSAGE = "パスワードは8文字以上で入力してください"
TOO_LONG_PASSWORD_ERROR_MESSAGE = "パスワードは255文字以内で入力してください"
BLANK_PASSWORD_ERROR_MESSAGE = "パスワードが空です"
MAX_NAME_LENGTH = 255
MAX_EMAIL_LENGTH = 255
MAX_PASSWORD_LENGTH = 255
MIN_PASSWORD_LENGTH = 8


def test_signup_validate_password():
    serializer = SignUpSerializer()

    # 255文字のnameを生成
    valid_password = "a" * MAX_PASSWORD_LENGTH
    assert serializer.validate_password(valid_password) == valid_password

    with pytest.raises(ValidationError, match=TOO_SHORT_PASSWORD_ERROR_MESSAGE):
        # 7文字のpasswordを生成
        too_short_password = "a" * (MIN_PASSWORD_LENGTH - 1)
        serializer.validate_password(too_short_password)

    with pytest.raises(ValidationError, match=TOO_LONG_PASSWORD_ERROR_MESSAGE):
        # 256文字のpasswordを生成
        too_long_password = "a" * (MAX_PASSWORD_LENGTH + 1)
        serializer.validate_password(too_long_password)


@pytest.mark.django_db
def test_signup_serializer():
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "password",
    }
    serializer = SignUpSerializer(data=input_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_signup_validate_name():
    serializer = SignUpSerializer()

    # 255文字のnameを生成
    valid_name = "a" * MAX_NAME_LENGTH
    assert serializer.validate_name(valid_name) == valid_name

    with pytest.raises(ValidationError, match=BLANK_NAME_ERROR_MESSAGE):
        serializer.validate_name("")

    with pytest.raises(ValidationError, match=TOO_LONG_NAME_ERROR_MESSAGE):
        # 256文字のnameを生成
        too_long_name = "a" * (MAX_NAME_LENGTH + 1)
        serializer.validate_name(too_long_name)


@pytest.mark.django_db
def test_signup_validate_email():
    serializer = SignUpSerializer()

    # 255文字のemailを生成
    valid_email = "a" * (MAX_EMAIL_LENGTH - len("@test.com")) + "@test.com"
    assert serializer.validate_email(valid_email) == valid_email

    with pytest.raises(ValidationError, match=BLANK_EMAIL_ERROR_MESSAGE):
        serializer.validate_email("")

    with pytest.raises(ValidationError, match=TOO_LONG_EMAIL_ERROR_MESSAGE):
        # 256文字のemailを生成
        too_long_email = "a" * (MAX_EMAIL_LENGTH - len("@test.com") + 1) + "@test.com"
        serializer.validate_email(too_long_email)


@pytest.mark.django_db
def test_signup_error_message_with_blank_name():
    invalid_input_data = {
        "name": "",
        "email": "test@test.com",
        "password": "password",
    }
    serializer = SignUpSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["name"][0]) == BLANK_NAME_ERROR_MESSAGE


@pytest.mark.django_db
def test_signup_error_message_with_blank_email():
    invalid_input_data = {
        "name": "testuser",
        "email": "",
        "password": "password",
    }
    serializer = SignUpSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "email" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["email"][0]) == BLANK_EMAIL_ERROR_MESSAGE


@pytest.mark.django_db
def test_signup_error_message_with_blank_password():
    invalid_input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "",
    }
    serializer = SignUpSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "password" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["password"][0]) == BLANK_PASSWORD_ERROR_MESSAGE


@pytest.mark.django_db
def test_signup_error_message_with_too_long_name():
    # 256文字のnameを生成
    too_long_name = "a" * (MAX_NAME_LENGTH + 1)
    invalid_input_data = {
        "name": too_long_name,
        "email": "test@test.com",
        "password": "password",
    }
    serializer = SignUpSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["name"][0]) == TOO_LONG_NAME_ERROR_MESSAGE


@pytest.mark.django_db
def test_signup_error_message_with_too_long_email():
    # 256文字のemailを生成
    too_long_email = "a" * (MAX_EMAIL_LENGTH - len("@test.com") + 1) + "@test.com"
    invalid_input_data = {
        "name": "testuser",
        "email": too_long_email,
        "password": "password",
    }
    serializer = SignUpSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "email" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["email"][0]) == TOO_LONG_EMAIL_ERROR_MESSAGE


@pytest.mark.django_db
def test_signup_error_message_with_too_long_password():
    # 256文字のpasswordを生成
    too_long_password = "a" * (MAX_PASSWORD_LENGTH + 1)
    invalid_input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": too_long_password,
    }
    serializer = SignUpSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "password" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["password"][0]) == TOO_LONG_PASSWORD_ERROR_MESSAGE


@pytest.mark.django_db
def test_signup_error_message_with_too_short_password():
    # 7文字のpasswordを生成
    too_short_password = "a" * (MIN_PASSWORD_LENGTH - 1)
    invalid_input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": too_short_password,
    }
    serializer = SignUpSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "password" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["password"][0]) == TOO_SHORT_PASSWORD_ERROR_MESSAGE


@pytest.mark.django_db
def test_include_token_in_response():
    User = get_user_model()
    new_user = User.objects.create_user(
        name="testuser",
        email="test@test.com",
        password="password",
    )

    serializer = SignUpSerializer(instance=new_user)
    response = serializer.to_representation(new_user)
    assert "refresh_token" in response
    assert "access_token" in response


@pytest.mark.django_db
def test_update_user_validate_name():
    serializer = UserUpdateSerializer()

    # 255文字のnameを生成
    valid_name = "a" * MAX_NAME_LENGTH
    assert serializer.validate_name(valid_name) == valid_name

    with pytest.raises(ValidationError, match=BLANK_NAME_ERROR_MESSAGE):
        serializer.validate_name("")

    with pytest.raises(ValidationError, match=TOO_LONG_NAME_ERROR_MESSAGE):
        # 256文字のnameを生成
        too_long_name = "a" * (MAX_NAME_LENGTH + 1)
        serializer.validate_name(too_long_name)


@pytest.mark.django_db
def test_update_user_validate_email():
    serializer = UserUpdateSerializer()

    # 255文字のemailを生成
    valid_email = "a" * (MAX_EMAIL_LENGTH - len("@test.com")) + "@test.com"
    assert serializer.validate_email(valid_email) == valid_email

    with pytest.raises(ValidationError, match=BLANK_EMAIL_ERROR_MESSAGE):
        serializer.validate_email("")

    with pytest.raises(ValidationError, match=TOO_LONG_EMAIL_ERROR_MESSAGE):
        # 256文字のemailを生成
        too_long_email = "a" * (MAX_EMAIL_LENGTH - len("@test.com") + 1) + "@test.com"
        serializer.validate_email(too_long_email)


@pytest.mark.django_db
def test_update_user_error_message_with_too_long_name():
    # 256文字のnameを生成
    too_long_name = "a" * (MAX_NAME_LENGTH + 1)
    invalid_input_data = {
        "name": too_long_name,
        "email": "test@test.com",
    }
    serializer = UserUpdateSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["name"][0]) == TOO_LONG_NAME_ERROR_MESSAGE


@pytest.mark.django_db
def test_update_user_error_message_with_too_long_email():
    # 256文字のemailを生成
    too_long_email = "a" * (MAX_EMAIL_LENGTH - len("@test.com") + 1) + "@test.com"
    invalid_input_data = {
        "name": "testuser",
        "email": too_long_email,
    }
    serializer = UserUpdateSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "email" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["email"][0]) == TOO_LONG_EMAIL_ERROR_MESSAGE


@pytest.mark.django_db
def test_update_user_error_message_with_blank_name():
    invalid_input_data = {
        "name": "",
        "email": "test@test.com",
    }
    serializer = UserUpdateSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["name"][0]) == BLANK_NAME_ERROR_MESSAGE


@pytest.mark.django_db
def test_update_user_error_message_with_blank_email():
    invalid_input_data = {
        "name": "testuser",
        "email": "",
    }
    serializer = UserUpdateSerializer(data=invalid_input_data)
    assert serializer.is_valid() is False
    assert "email" in serializer.errors

    # エラーメッセージが正しいか検証
    assert str(serializer.errors["email"][0]) == BLANK_EMAIL_ERROR_MESSAGE
