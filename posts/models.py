from django.db import models

from accounts.models import CustomUser
from chat_rooms.models import Room


class Post(models.Model):
    """投稿を管理"""

    TEXT = "text"
    IMAGE = "image"
    TEXT_IMAGE = "text_image"
    MESSAGE_TYPE_CHOICES = ((TEXT, "テキスト"), (IMAGE, "画像"), (TEXT_IMAGE, "テキストと画像"))

    message = models.TextField(
        verbose_name="メッセージ",
        max_length=40000,
        blank=True,
        null=True,
    )
    image = models.FileField(
        verbose_name="画像",
        upload_to="images/",  # 本番環境ではS3にアップロード
        max_length=255,
        blank=True,
        null=True,
    )
    message_type = models.CharField(
        verbose_name="メッセージタイプ",
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
    )
    created_at = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = "posts"
        verbose_name = "投稿"
