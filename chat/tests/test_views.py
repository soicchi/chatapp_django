import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from chat.models import Room, RoomMember


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    User = get_user_model()
    user = User.objects.create_user(
        name="test_user",
        email="test@test.com",
        password="password",
    )

    return user


@pytest.mark.django_db
def test_leave_room_success(api_client, test_user):
    # テストユーザー作成
    User = get_user_model()
    test_user2 = User.objects.create_user(
        name="test_user2",
        email="test2@test.com",
        password="password",
    )

    # テストルームを作成
    room = Room.objects.create(name="test_room", admin_user=test_user)

    # RoomMemberのレコードも追加
    RoomMember.objects.create(user_id=test_user.id, room_id=room.id)
    RoomMember.objects.create(user_id=test_user2.id, room_id=room.id)

    input_data = {
        "user_id": test_user.id,
        "room_id": room.id,
    }

    # ユーザー認証を通す
    api_client.force_authenticate(user=test_user)
    response = api_client.post(reverse("chat:leave_room"), input_data, format="json")
    assert response.status_code == 204
    assert response.data["message"] == "チャットルームを退出しました"

    # チャットルームに該当ユーザーが含まれていないか検証
    room.refresh_from_db()
    assert not test_user in room.users.all()


@pytest.mark.django_db
def test_leave_room_failure(api_client, test_user):
    # テストルームを作成
    room = Room.objects.create(name="test_room", admin_user=test_user)

    # RoomMemberのレコードも追加
    RoomMember.objects.create(user_id=test_user.id, room_id=room.id)

    input_data = {
        "user_id": "",
        "room_id": room.id,
    }

    # ユーザーの認証を通す
    api_client.force_authenticate(user=test_user)
    response = api_client.post(reverse("chat:leave_room"), input_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_leave_room_unauthenticated(api_client, test_user):
    # テストルーム作成
    room = Room.objects.create(name="test_room", admin_user=test_user)

    # RoomMemberのレコードも追加
    RoomMember.objects.create(user_id=test_user.id, room_id=room.id)

    input_data = {
        "user_id": test_user.id,
        "room_id": room.id,
    }

    # ユーザー認証を通す
    response = api_client.post(reverse("chat:leave_room"), input_data, format="json")
    assert response.status_code == 401
