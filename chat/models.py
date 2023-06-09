from django.db import models

from accounts.models import CustomUser


class Room(models.Model):
    name = models.CharField(verbose_name="ルーム名", max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now=True, null=False, blank=False)
    admin_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="admin_rooms")
    users = models.ManyToManyField(
        CustomUser,
        through="RoomMember",
        through_fields=("room", "user")
    )

    class Meta:
        db_table = "rooms"
        verbose_name = "チャットルーム"

    def __str__(self) -> str:
        return self.name


class RoomMember(models.Model):
    entry_datetime = models.DateTimeField(verbose_name="入室日", auto_now=True, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = "room_member"
