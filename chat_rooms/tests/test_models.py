import pytest
from django.contrib.auth import get_user_model

from chat_rooms.models import Room, RoomMember


@pytest.mark.django_db
def test_fetch_room():
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
        admin_user=user,
    )

    fetched_room = Room.fetch_room(room.id)
    assert fetched_room == room

    with pytest.raises(ValueError):
        Room.fetch_room(room.id + 1)
        assert "チャットルームが見つかりません" in str(ValueError)


@pytest.mark.django_db
def test_create_room():
    # テストユーザー作成
    User = get_user_model()
    user = User.objects.create_user(
        name="test_user",
        email="test@test.com",
        password="password",
    )

    room = Room.objects.create(
        name="test_room",
        admin_user=user,
    )
    assert room.admin_user == user
    assert room.name == "test_room"
    assert room in Room.objects.all()


@pytest.mark.django_db
def test_fetch_room_member():
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
        admin_user=user,
    )
    RoomMember.objects.create(user_id=user.id, room_id=room.id)

    fetched_room_member = RoomMember.fetch_room_member(user_id=user.id, room_id=room.id)
    assert fetched_room_member.room == room
    assert fetched_room_member.user == user

    with pytest.raises(ValueError):
        RoomMember.fetch_room_member(user_id=user.id, room_id=room.id + 1)
        assert "RoomMemberが見つかりません" in str(ValueError)


@pytest.mark.django_db
def test_fetch_room_members():
    # テストユーザー作成
    User = get_user_model()
    user1 = User.objects.create_user(
        name="test_user1",
        email="test1@test.com",
        password="password",
    )
    user2 = User.objects.create_user(
        name="test_user2",
        email="test2@test.com",
        password="password",
    )

    # テストルーム作成
    room = Room.objects.create(
        name="test_room1",
        admin_user=user1,
    )
    room_member1 = RoomMember.objects.create(user_id=user1.id, room_id=room.id)
    room_member2 = RoomMember.objects.create(user_id=user2.id, room_id=room.id)

    fetched_room_members = RoomMember.fetch_room_members(room.id)
    assert room_member1 in fetched_room_members
    assert room_member2 in fetched_room_members

    with pytest.raises(ValueError):
        RoomMember.fetch_room_members(room_id=room.id + 1)
        assert "RoomMemberが見つかりません" in str(ValueError)
