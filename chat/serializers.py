from rest_framework import serializers

from .fields import CustomNameField
from .models import Room, RoomMember


class CreateRoomSerializer(serializers.ModelSerializer):
    """チャットルームを作成"""

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


class LeaveRoomSerializer(serializers.Serializer):
    """チャットルームを退出"""

    user_id = serializers.IntegerField()
    room_id = serializers.IntegerField()

    def validate(self, data: dict) -> dict:
        user_id = data["user_id"]
        room_id = data["room_id"]

        # 該当するRoomMemberレコードの存在を検証
        room_member = RoomMember.objects.filter(user_id=user_id, room_id=room_id).first()
        if room_member is None:
            raise serializers.ValidationError("指定したユーザーがチャットルームのメンバーに存在しません")

        return data

    def destroy(self, validated_data: dict) -> None:
        user_id = validated_data["user_id"]
        room_id = validated_data["room_id"]
        room_member = RoomMember.objects.filter(user_id=user_id, room_id=room_id).first()
        room_member.delete()
