from rest_framework import serializers


class CustomNameField(serializers.CharField):
    default_error_messages = {
        "blank": "チャットルーム名が空です",
        "max_length": "チャットルーム名は255文字以内で入力してください",
    }
