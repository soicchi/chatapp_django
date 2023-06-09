# Generated by Django 4.2.1 on 2023-06-09 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="ルーム名")),
                (
                    "created_at",
                    models.DateTimeField(auto_now=True, verbose_name="作成日時"),
                ),
                (
                    "admin_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="admin_rooms",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "チャットルーム",
                "db_table": "rooms",
            },
        ),
        migrations.CreateModel(
            name="RoomMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entry_datetime",
                    models.DateTimeField(auto_now=True, verbose_name="入室日"),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.room"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "room_member",
            },
        ),
        migrations.AddField(
            model_name="room",
            name="users",
            field=models.ManyToManyField(
                through="chat.RoomMember", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
