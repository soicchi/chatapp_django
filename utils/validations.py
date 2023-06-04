from rest_framework import serializers


class PasswordValidation:
    def __init__(self, input_password: str) -> None:
        self.min_length = 8
        self.input_password = input_password

    def validate(self) -> None:
        self._validate_length()

    # パスワードは8文字以上
    def _validate_length(self) -> None:
        if len(self.input_password) < self.min_length:
            raise serializers.ValidationError("パスワードは8文字以上で入力してください")
