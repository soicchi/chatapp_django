from django.contrib.auth import get_user_model
from rest_framework import serializers


class PasswordValidation:
    def __init__(self, input_password: str) -> None:
        self.max_length: int = 255
        self.min_length: int = 8
        self.password: str = input_password

    def validate(self) -> None:
        self._validate_length()

    def _validate_length(self) -> None:
        if len(self.password) < self.min_length:
            raise serializers.ValidationError("パスワードは8文字以上で入力してください")

        if len(self.password) > self.max_length:
            raise serializers.ValidationError("パスワードは255文字以内で入力してください")


class UserNameValidation:
    def __init__(self, input_name: str) -> None:
        self.max_length: int = 255
        self.name: str = input_name

    def validate(self) -> None:
        self._validate_length()
        self._validate_blank()

    def _validate_length(self) -> None:
        if len(self.name) > self.max_length:
            raise serializers.ValidationError("ユーザー名は255文字以内で入力してください")

    def _validate_blank(self) -> None:
        if self.name == "":
            raise serializers.ValidationError("ユーザー名が空です")


class EmailValidation:
    def __init__(self, input_email: str) -> None:
        self.max_length: int = 255
        self.email: str = input_email

    def validate(self) -> None:
        self._validate_length()
        self._validate_blank()
        self._validate_unique()

    def _validate_length(self) -> None:
        if len(self.email) > self.max_length:
            raise serializers.ValidationError("メールアドレスは255文字以内で入力してください")

    def _validate_blank(self) -> None:
        if self.email == "":
            raise serializers.ValidationError("メールアドレスが空です")

    def _validate_unique(self) -> None:
        User = get_user_model()
        exists_email = User.objects.filter(email=self.email).exists()
        if exists_email:
            raise serializers.ValidationError("すでに使用されているメールアドレスです")
