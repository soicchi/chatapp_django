import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from chat.serializers import CreateRoomSerializer, LeaveRoomSerializer
from chat.models import Room, RoomMember

BLANK_NAME_ERROR_MESSAGE = "チャットルーム名が空です"


@pytest.fixture
def test_user():
    User = get_user_model()
    user = User.objects.create_user(
        name="test_user",
        email="test@test.com",
        password="password"
    )

    return user


@pytest.mark.django_db
def test_create_room(test_user):
    input_data = {"name": "test_room", "admin_user": test_user.id}
    serializer = CreateRoomSerializer(data=input_data)
    assert serializer.is_valid()

    # インスタンス生成
    room = serializer.save()
    assert room.name == input_data["name"]
    assert room.admin_user == test_user
    assert test_user in room.users.all()


@pytest.mark.django_db
def test_leave_room(test_user):
    # テストルームを作成
    room = Room.objects.create(
        name="test_room",
        admin_user=test_user,
    )

    # RoomMemberも登録
    RoomMember.objects.create(user_id=test_user.id, room_id=room.id)

    input_data = {
        "user_id": test_user.id,
        "room_id": room.id,
    }
    serializer = LeaveRoomSerializer(data=input_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_validate_leave_room_():
    # テストユーザーを作成
    User = get_user_model()
    user1 = User.objects.create_user(
        name="test_user1",
        email="user1@test.com",
        password="password",
    )
    user2 = User.objects.create_user(
        name="test_user2",
        email="user2@test.com",
        password="password",
    )

    # テスト用にあらかじめチャットルーム作成
    room = Room.objects.create(name="test_room", admin_user=user1)

    input_data = {
        "user_id": user2.id,
        "room_id": room.id,
    }
    serializer = LeaveRoomSerializer(data=input_data)

    with pytest.raises(ValidationError, match="指定したユーザーがチャットルームのメンバーに存在しません"):
        serializer.validate(data=input_data)
