from rest_framework import serializers

from .fields import CustomNameField
from .models import Room, RoomMember
from .services import RoomManagerService, RoomMembershipService
from accounts.models import CustomUser


class CreateRoomSerializer(serializers.ModelSerializer):
    """チャットルームを作成"""

    name = CustomNameField()

    class Meta:
        model = Room
        fields = ["name", "admin_user"]

    def create(self, validated_data: dict) -> Room:
        room_name = validated_data["name"]
        admin_user = validated_data["admin_user"]

        return RoomManagerService.create_room(
            room_name=room_name, admin_user=admin_user
        )


class JoinRoomSerializer(serializers.Serializer):
    """チャットルームに参加"""

    user_id = serializers.IntegerField()
    room_id = serializers.IntegerField()

    def validate_user_id(self, user_id: int) -> int:
        try:
            CustomUser.fetch_user(user_id)
        except ValueError:
            raise serializers.ValidationError("指定されたユーザーIDが見つかりません")

        return user_id

    def validate_room_id(self, room_id: int) -> int:
        try:
            Room.fetch_room(room_id)
        except ValueError:
            raise serializers.ValidationError("指定されたルームIDが見つかりません")

        return room_id

    def create(self, validated_data: dict) -> None:
        user_id = validated_data["user_id"]
        room_id = validated_data["room_id"]

        target_room = Room.fetch_room(room_id)
        room_membership = RoomMembershipService(target_room)
        room_membership.join_room(user_id)


class LeaveRoomSerializer(serializers.Serializer):
    """チャットルームを退出"""

    user_id = serializers.IntegerField()
    room_id = serializers.IntegerField()

    def validate(self, data: dict) -> dict:
        user_id = data["user_id"]
        room_id = data["room_id"]

        # 該当するRoomMemberレコードの存在を検証
        try:
            RoomMember.fetch_room_member(user_id=user_id, room_id=room_id)
        except ValueError:
            raise serializers.ValidationError("指定されたユーザーIDとルームIDの組み合わせが見つかりません")

        return data

    def destroy(self, validated_data: dict) -> None:
        user_id = validated_data["user_id"]
        room_id = validated_data["room_id"]

        target_room = Room.fetch_room(room_id)
        room_membership = RoomMembershipService(target_room)
        room_membership.leave_room(user_id)
