from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from utils.validations import PasswordValidation


class SignUpSerializer(serializers.ModelSerializer):
    """新規登録用のシリアライザ"""

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "ユーザー名が空です",
                    "max_length": "ユーザー名は255文字以内で入力してください",
                }
            },
            "email": {
                "error_messages": {
                    "blank": "メールアドレスが空です",
                    "max_length": "メールアドレスは255文字以内で入力してください",
                }
            },
            "password": {
                "write_only": True,
                "error_messages": {
                    "blank": "パスワードが空です",
                    "max_length": "パスワードは255文字以内で入力してください",
                },
            },
        }

    def create(self, validated_data: dict) -> CustomUser:
        new_user = CustomUser.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return new_user

    def validate_password(self, input_password: str) -> str:
        password_validation = PasswordValidation(input_password)
        password_validation.validate()

        return input_password

    def to_representation(self, instance: CustomUser) -> CustomUser:
        # リフレッシュトークンとJWTをレスポンスに含める
        refresh_token = RefreshToken.for_user(instance)
        new_user = super().to_representation(instance)
        new_user["refresh_token"] = str(refresh_token)
        new_user["access_token"] = str(refresh_token.access_token)

        return new_user


class UserListSerializer(serializers.ModelSerializer):
    """ユーザー一覧用のシリアライザ"""

    class Meta:
        model = CustomUser
        fields = ["id", "name"]


class UserRetrieveSerializer(serializers.ModelSerializer):
    """ユーザー詳細用のシリアライザ"""

    class Meta:
        model = CustomUser
        fields = ["id", "name"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """ユーザーデータ更新用のシリアライザ"""

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]

    def update(self, instance: CustomUser, validated_data: dict) -> CustomUser:
        pass
