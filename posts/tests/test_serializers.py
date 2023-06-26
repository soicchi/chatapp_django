import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from rest_framework.exceptions import ValidationError

from chat_rooms.models import Room
from posts.serializers import PostCreateSerializer


@pytest.fixture
def initialize():
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

    return {"user": user, "room": room}


@pytest.mark.django_db
def test_create_post_success(initialize):
    # request内にユーザー情報をセット
    request = RequestFactory().post("/api/v1/posts/")
    request.user = initialize["user"]
    input_data = {
        "message": "テストメッセージ",
        "room_id": initialize["room"].id,
    }
    serializer = PostCreateSerializer(data=input_data, context={"request": request})
    assert serializer.is_valid()

    post = serializer.save()
    assert post.message == "テストメッセージ"
    assert post.user == initialize["user"]
    assert post.room == initialize["room"]


@pytest.mark.django_db
def test_validate_room_id(initialize):
    # request内にユーザー情報をセット
    request = RequestFactory().post("/api/v1/posts/")
    request.user = initialize["user"]
    input_data = {
        "message": "テストメッセージ",
        "room_id": initialize["room"].id + 1,
    }

    serializer = PostCreateSerializer(data=input_data, context={"request": request})
    with pytest.raises(ValidationError, match="指定されたルームIDが見つかりません"):
        serializer.is_valid(raise_exception=True)
