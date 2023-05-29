from rest_framework import serializers

from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    """新規登録用のシリアライザ"""

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate_password(self, input_password: str) -> str:
        min_length = 8
        if len(input_password) < min_length:
            raise serializers.ValidationError("パスワードは8文字以上で入力してください")

        return input_password
