import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from chat_rooms.models import Room, RoomMember

BASE_ROOMS_URI_NAME = "rooms"


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
def test_create_room_success(api_client, test_user):
    input_data = {
        "name": "test_room",
        "admin_user": test_user.id,
    }

    # ユーザー認証を通す
    api_client.force_authenticate(user=test_user)
    response = api_client.post(
        reverse(f"chat_rooms:{BASE_ROOMS_URI_NAME}-list"), input_data, format="json"
    )
    assert response.status_code == 201
    assert response.data["name"] == "test_room"
    assert response.data["admin_user"] == test_user.id


@pytest.mark.django_db
def test_create_room_unauthenticated(api_client, test_user):
    input_data = {
        "name": "test_room",
        "admin_user": test_user.id,
    }
    response = api_client.post(
        reverse(f"chat_rooms:{BASE_ROOMS_URI_NAME}-list"), input_data, format="json"
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_rooms_success(api_client, test_user):
    # テストルームを作成
    room1 = Room.objects.create(name="test_room1", admin_user=test_user)
    room2 = Room.objects.create(name="test_room2", admin_user=test_user)

    # ユーザー認証を通す
    api_client.force_authenticate(user=test_user)
    response = api_client.get(reverse(f"chat_rooms:{BASE_ROOMS_URI_NAME}-list"))
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == room1.name
    assert response.data[0]["admin_user"] == test_user.id
    assert response.data[1]["name"] == room2.name
    assert response.data[1]["admin_user"] == test_user.id


@pytest.mark.django_db
def test_list_rooms_unauthenticated(api_client, test_user):
    # テストルームを作成
    Room.objects.create(name="test_room1", admin_user=test_user)
    Room.objects.create(name="test_room2", admin_user=test_user)

    response = api_client.get(reverse(f"chat_rooms:{BASE_ROOMS_URI_NAME}-list"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_detail_room_success(api_client, test_user):
    # テストルームを作成
    room = Room.objects.create(name="test_room", admin_user=test_user)

    # ユーザー認証を通す
    api_client.force_authenticate(user=test_user)
    response = api_client.get(
        reverse(f"chat_rooms:{BASE_ROOMS_URI_NAME}-detail", kwargs={"pk": room.id})
    )
    assert response.status_code == 200
    assert response.data["id"] == room.id
    assert response.data["name"] == room.name
    assert response.data["admin_user"] == test_user.id


@pytest.mark.django_db
def test_detail_room_unauthenticated(api_client, test_user):
    # テストルームを作成
    room = Room.objects.create(name="test_room", admin_user=test_user)

    response = api_client.get(
        reverse(f"chat_rooms:{BASE_ROOMS_URI_NAME}-detail", kwargs={"pk": room.id})
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_join_room_authenticated(api_client, test_user):
    # テストユーザー作成
    User = get_user_model()
    test_user2 = User.objects.create_user(
        name="test_user2",
        email="test2@test.com",
        password="password",
    )

    # テストルームを作成
    room = Room.objects.create(name="test_room", admin_user=test_user)
    RoomMember.objects.create(user_id=test_user.id, room_id=room.id)

    api_client.force_authenticate(user=test_user2)
    input_data = {
        "user_id": test_user2.id,
        "room_id": room.id,
    }
    response = api_client.post(
        reverse("chat_rooms:join_room"), input_data, format="json"
    )
    assert response.status_code == 201
    assert response.data["message"] == "チャットルームに参加しました"


@pytest.mark.django_db
def test_join_room_unauthenticated(api_client, test_user):
    # テストユーザー作成
    User = get_user_model()
    test_user2 = User.objects.create_user(
        name="test_user2",
        email="test2@test.com",
        password="password",
    )

    # テストルームを作成
    room = Room.objects.create(name="test_room", admin_user=test_user)
    RoomMember.objects.create(user_id=test_user.id, room_id=room.id)

    input_data = {
        "user_id": test_user2.id,
        "room_id": room.id,
    }
    response = api_client.post(
        reverse("chat_rooms:join_room"), input_data, format="json"
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_join_room_failure(api_client, test_user):
    # テストユーザー作成
    User = get_user_model()
    test_user2 = User.objects.create_user(
        name="test_user2",
        email="test2@test.com",
        password="password",
    )

    # テストルームを作成
    room = Room.objects.create(name="test_room", admin_user=test_user)
    RoomMember.objects.create(user_id=test_user.id, room_id=room.id)

    api_client.force_authenticate(user=test_user2)

    # 存在しないルームIDを指定
    input_data = {
        "user_id": test_user2.id,
        "room_id": room.id + 1,
    }
    response = api_client.post(
        reverse("chat_rooms:join_room"), input_data, format="json"
    )
    assert response.status_code == 400


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
    response = api_client.post(
        reverse("chat_rooms:leave_room"), input_data, format="json"
    )
    assert response.status_code == 204
    assert response.data["message"] == "チャットルームを退出しました"

    # チャットルームに該当ユーザーが含まれていないか検証
    room.refresh_from_db()
    assert test_user not in room.users.all()


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
    response = api_client.post(
        reverse("chat_rooms:leave_room"), input_data, format="json"
    )
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
    response = api_client.post(
        reverse("chat_rooms:leave_room"), input_data, format="json"
    )
    assert response.status_code == 401
