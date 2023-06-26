import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from chat_rooms.models import Room

BASE_POSTS_URI_NAME = "posts"


@pytest.fixture
def api_client():
    return APIClient()


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
def test_create_post_authenticated(api_client, initialize):
    # テストユーザーでログイン
    api_client.force_authenticate(user=initialize["user"])
    input_data = {
        "message": "テストメッセージ",
        "room_id": initialize["room"].id,
    }
    response = api_client.post(
        reverse(f"posts:{BASE_POSTS_URI_NAME}-list"), data=input_data, format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_post_unauthenticated(api_client, initialize):
    input_data = {
        "message": "テストメッセージ",
        "room_id": initialize["room"].id,
    }
    response = api_client.post(
        reverse(f"posts:{BASE_POSTS_URI_NAME}-list"), data=input_data, format="json"
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_fetch_list_post_authenticated(api_client, initialize):
    # テストユーザーでログイン
    api_client.force_authenticate(user=initialize["user"])
    response = api_client.get(
        reverse(f"posts:{BASE_POSTS_URI_NAME}-list"), format="json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_fetch_list_post_unauthenticated(api_client, initialize):
    response = api_client.get(
        reverse(f"posts:{BASE_POSTS_URI_NAME}-list"), format="json"
    )
    assert response.status_code == 401
