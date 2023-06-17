from django.db import transaction
from .models import CustomUser, Room, RoomMember


class RoomManagerService:
    """Roomの作成、削除、更新などの基本的な操作を行うクラス"""

    @staticmethod
    @transaction.atomic
    def create_room(room_name: str, admin_user: CustomUser) -> Room:
        room = Room.create_room(name=room_name, user=admin_user)

        # チャットルームのメンバーとしても管理ユーザーを追加
        room.users.add(admin_user)

        return room


class RoomMembershipService:
    """RoomMemberの操作を行うクラス"""

    def __init__(self, room: Room) -> None:
        self.room = room

    def assign_new_admin(self, admin_user_id: int) -> None:
        """新しい管理者をチャットルームに保存

        Args:
            admin_user_id (int): 現在の管理者ユーザーのID

        Raises:
            ValueError: 入力されたadmin_user_idが管理者ユーザーIDではない場合
            ValueError: 管理者ユーザー以外にユーザーが存在しない場合
        """

        new_admin_user = self._select_admin_user(admin_user_id)
        self._set_admin_user(new_admin_user)

    def _select_admin_user(self, admin_user_id: int) -> CustomUser:
        """チャットルーム内のユーザーから管理者を選択

        Args:
            admin_user_id (int): 現在の管理者ユーザーID

        Raises:
            ValueError: 管理ユーザー以外にチャットルームにユーザーが存在しない場合

        Returns:
            CustomUser: 新しい管理ユーザーオブジェクト
        """

        room_members = RoomMember.fetch_room_members(room_id=self.room.id)

        # 現在の管理ユーザーを除いたユーザーの中で最も入室日が古いレコードを取得
        oldest_entry = room_members.exclude(user_id=admin_user_id).order_by("entry_datetime").first()
        if not oldest_entry:
            raise ValueError(f"チャットルームにユーザーが存在しません。room_id: {self.room.id}")

        return oldest_entry.user

    def _set_admin_user(self, new_admin_user: CustomUser) -> None:
        """新しいユーザーをチャットルームの管理者に設定

        Args:
            new_admin_user (CustomUser): 新しく管理ユーザーになるユーザーオブジェクト

        Raises:
            ValueError: チャットルームが存在しない場合
        """

        self.room.admin_user = new_admin_user
        self.room.save()

    def leave_room(self, user_id: int) -> None:
        """チャットルームを退出

        Args:
            user_id (int): 退出するユーザーID
        """

        if self.room.admin_user.id == user_id:
            self.assign_new_admin(user_id)

        room_member = RoomMember.fetch_room_member(user_id=user_id, room_id=self.room.id)
        room_member.delete()

        # チャットルームにユーザーが残っていない場合、チャットルームも削除
        if self.room.users.count() == 0:
            self.room.delete()
