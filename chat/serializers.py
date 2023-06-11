from rest_framework import serializers

from .fields import CustomNameField
from .models import Room


class CreateRoomSerializer(serializers.ModelSerializer):
    """チャットルームを作成する"""

    name = CustomNameField()

    class Meta:
        model = Room
        fields = ["name", "admin_user"]

    def create(self, validated_data: dict) -> Room:
        room_name = validated_data["name"]
        admin_user = validated_data["admin_user"]
        room = Room.objects.create(name=room_name, admin_user=admin_user)

        # 管理者をチャットルームのメンバーとして追加
        room.users.add(admin_user)

        return room
