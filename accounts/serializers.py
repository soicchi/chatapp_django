from rest_framework import serializers

from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    """新規登録用のシリアライザ"""

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "ユーザー名の入力は必須です",
                    "max_length": "ユーザー名は255文字以内で入力してください",
                }
            },
            "email": {
                "error_messages": {
                    "blank": "メールアドレスの入力は必須です",
                    "max_length": "メールアドレスは255文字以内で入力してください",
                }
            },
            "password": {
                "write_only": True,
                "error_messages": {
                    "blank": "パスワードの入力は必須です",
                    "max_length": "パスワードは255文字以内で入力してください",
                },
            },
        }

    def validate_password(self, input_password: str) -> str:
        min_length = 8
        if len(input_password) < min_length:
            raise serializers.ValidationError("パスワードは8文字以上で入力してください")

        return input_password
