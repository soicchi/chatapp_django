from django.db import models
from django.db.models import QuerySet

from accounts.models import CustomUser


class Room(models.Model):
    """チャットルームを管理"""

    name = models.CharField(verbose_name="ルーム名", max_length=255)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    admin_user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="admin_rooms"
    )
    users = models.ManyToManyField(
        CustomUser, through="RoomMember", through_fields=("room", "user")
    )

    class Meta:
        db_table = "rooms"
        verbose_name = "チャットルーム"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def fetch_room(cls, room_id: int) -> "Room":
        """チャットルームを取得

        Raises:
            ValueError: チャットルームが見つからない場合

        Returns:
            Room: チャットルームオブジェクト
        """

        room = cls.objects.filter(pk=room_id).first()
        if not room:
            raise ValueError(f"チャットルームが見つかりません。room_id: {room_id}")

        return room

    @classmethod
    def create_room(cls, name: str, user: CustomUser) -> "Room":
        """チャットルームを作成

        Args:
            name (str): チャットルーム名
            user (CustomUser): 管理ユーザーとして登録するユーザーオブジェクト

        Returns:
            Room: Roomオブジェクト
        """

        return Room.objects.create(name=name, admin_user=user)


class RoomMember(models.Model):
    """チャットルームとユーザーのリレーションを管理"""

    entry_datetime = models.DateTimeField(verbose_name="入室日", auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = "room_member"

    @classmethod
    def fetch_room_member(cls, user_id: int, room_id: int) -> "RoomMember":
        """RoomMemberオブジェクトを取得

        Args:
            user_id (int): ユーザーID

        Raises:
            ValueError: RoomMemberが見つからない場合

        Returns:
            RoomMember: RoomMemberオブジェクト
        """

        room_member = cls.objects.filter(user_id=user_id, room_id=room_id).first()
        if not room_member:
            raise ValueError(
                f"RoomMemberが見つかりません。room_id: {room_id}, user_id: {user_id}"
            )

        return room_member

    @classmethod
    def fetch_room_members(cls, room_id: int) -> QuerySet["RoomMember"]:
        """複数のRoomMemberオブジェクトを取得

        Args:
            user_id (int): ユーザーID

        Raises:
            ValueError: RoomMemberが見つからない場合

        Returns:
            RoomMember: 複数のRoomMemberオブジェクト
        """

        room_members = cls.objects.filter(room_id=room_id)
        if not room_members.exists():
            raise ValueError(f"RoomMemberが見つかりません。room_id: {room_id}")

        return room_members
