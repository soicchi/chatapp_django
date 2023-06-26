from chat_rooms.models import Room

from .models import Post


class PostManagerService:
    """Postモデルの基本的な作成、取得、更新、削除を行う"""

    def __init__(self, post_model=Post, room_model=Room) -> None:
        self.post_model = post_model
        self.room_model = room_model

    def create_post(self, message: str, user: int, room_id: int) -> Post:
        """投稿を作成

        Args:
            message (str): 投稿するテキストメッセージ
            user (int): 投稿するユーザーインスタンス
            room_id (int): 投稿するルームID

        Returns:
            Post: 投稿されたPostモデルのインスタンス
        """

        room = self.room_model.fetch_room(room_id)
        post = self.post_model.objects.create(message=message, user=user, room=room)

        return post
