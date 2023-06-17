import pytest
from django.contrib.auth import get_user_model

from chat.models import Room, RoomMember
from chat.services import RoomManagerService, RoomMembershipService


@pytest.mark.django_db
def test_create_room():
    # テストユーザー作成
    User = get_user_model()
    user = User.objects.create_user(
        name="test_user",
        email="test@test.com",
        password="password",
    )
    room =RoomManagerService.create_room(
        room_name="test_room",
        admin_user=user,
    )

    assert room.admin_user == user
    assert user in room.users.all()


@pytest.mark.django_db
def test_assign_new_admin():
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
    room = RoomManagerService.create_room(
        room_name="test_room",
        admin_user=user1,
    )
    RoomMember.objects.create(
        user=user2,
        room=room,
    )

    room_membership = RoomMembershipService(room)
    room_membership.assign_new_admin(admin_user_id=user1.id)
    assert room.admin_user == user2
    assert not room.admin_user == user1


@pytest.mark.django_db
def test_select_admin_user():
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
    room = RoomManagerService.create_room(
        room_name="test_room",
        admin_user=user1,
    )
    RoomMember.objects.create(
        user=user2,
        room=room,
    )

    room_membership = RoomMembershipService(room)
    new_admin_user = room_membership._select_admin_user(admin_user_id=user1.id)
    assert new_admin_user == user2
    assert not new_admin_user == user1


@pytest.mark.django_db
def test_set_admin_user():
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
    room = RoomManagerService.create_room(
        room_name="test_room",
        admin_user=user1,
    )
    RoomMember.objects.create(
        user=user2,
        room=room,
    )

    room_membership = RoomMembershipService(room)
    room_membership._set_admin_user(new_admin_user=user2)
    assert room.admin_user == user2


@pytest.mark.django_db
def test_leave_room_with_one_user():
    # テストユーザー作成
    User = get_user_model()
    user = User.objects.create_user(
        name="test_user",
        email="test@test.com",
        password="password",
    )

    # テストルーム作成
    room = RoomManagerService.create_room(
        room_name="test_room",
        admin_user=user,
    )

    room_membership = RoomMembershipService(room)
    room_membership.leave_room(user_id=user.id)
    assert not Room.objects.filter(pk=room.id).exists()
    assert not RoomMember.objects.filter(user_id=user.id).exists()


@pytest.mark.django_db
def test_leave_room_with_multiple_users():
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
    room = RoomManagerService.create_room(
        room_name="test_room",
        admin_user=user1,
    )
    RoomMember.objects.create(
        user=user2,
        room=room,
    )

    room_membership = RoomMembershipService(room)
    room_membership.leave_room(user_id=user1.id)
    assert room.admin_user == user2
    assert not user1 in room.users.all()
