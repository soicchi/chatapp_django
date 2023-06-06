from rest_framework import serializers


class CustomNameField(serializers.CharField):
    default_error_messages = {
        "blank": "ユーザー名が空です",
        "max_length": "ユーザー名は255文字以内で入力してください",
    }


class CustomEmailField(serializers.EmailField):
    default_error_messages = {
        "blank": "メールアドレスが空です",
        "max_length": "メールアドレスは255文字以内で入力してください",
    }


class CustomPasswordField(serializers.CharField):
    default_error_messages = {
        "blank": "パスワードが空です",
        "max_length": "パスワードは255文字以内で入力してください",
    }
