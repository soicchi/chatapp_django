from rest_framework import serializers

from chat_rooms.services import RoomManagerService

from .models import Post
from .services import PostManagerService


class PostCreateSerializer(serializers.ModelSerializer):
    """投稿を作成"""

    room_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ["id", "message", "room_id", "created_at"]

    def validate_room_id(self, room_id: int) -> int:
        room_manager = RoomManagerService()
        try:
            room_manager.fetch_room(room_id)
        except ValueError:
            raise serializers.ValidationError("指定されたルームIDが見つかりません")

        return room_id

    def create(self, validated_data: dict) -> Post:
        message = validated_data["message"]
        user = self.context["request"].user
        room_id = validated_data["room_id"]

        post_manager = PostManagerService()
        new_post = post_manager.create_post(
            message=message,
            user=user,
            room_id=room_id,
        )

        return new_post



