from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from utils.fields import accounts
from utils.validations import EmailValidation, PasswordValidation, UserNameValidation

from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    """新規登録用"""

    name = accounts.CustomNameField()
    email = accounts.CustomEmailField()
    password = accounts.CustomPasswordField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]

    def create(self, validated_data: dict) -> CustomUser:
        new_user = CustomUser.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return new_user

    def validate_name(self, input_name: str) -> str:
        name_validation = UserNameValidation(input_name)
        name_validation.validate()

        return input_name

    def validate_email(self, input_email: str) -> str:
        email_validation = EmailValidation(input_email)
        email_validation.validate()

        return input_email

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
    """ユーザー一覧用"""

    class Meta:
        model = CustomUser
        fields = ["id", "name"]


class UserRetrieveSerializer(serializers.ModelSerializer):
    """ユーザー詳細用"""

    class Meta:
        model = CustomUser
        fields = ["id", "name"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """ユーザーデータ更新用"""

    name = accounts.CustomNameField()
    email = accounts.CustomEmailField()

    class Meta:
        model = CustomUser
        fields = ["name", "email"]

    def update(self, instance: CustomUser, validated_data: dict) -> CustomUser:
        instance.name = validated_data["name"]
        instance.email = validated_data["email"]
        instance.save()

        return instance

    def validate_name(self, input_name: str) -> str:
        name_validation = UserNameValidation(input_name)
        name_validation.validate()

        return input_name

    def validate_email(self, input_email: str) -> str:
        email_validation = EmailValidation(input_email)
        email_validation.validate()

        return input_email


class UserDestroySerializer(serializers.Serializer):
    """ユーザーデータ削除用"""

    def destroy(self, instance):
        instance.delete()
