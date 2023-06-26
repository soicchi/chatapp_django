import pytest
from django.contrib.auth import get_user_model

from chat_rooms.models import Room
from posts.services import PostManagerService


@pytest.mark.django_db
def test_create_post():
    # テストユーザー作成
    User = get_user_model()
    user = User.objects.create_user(
        name="test_user",
        email="test@test.com",
        password="password",
    )

    # テストルーム作成
    room = Room.objects.create(
        name="test_room",
        admin_user_id=user.id,
    )

    post_manager = PostManagerService()
    post = post_manager.create_post(
        message="テストメッセージ",
        user=user,
        room_id=room.id,
    )

    assert post.message == "テストメッセージ"
    assert post.user == user
    assert post.room == room
