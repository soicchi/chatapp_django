import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.serializers import UserListSerializer, UserRetrieveSerializer

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        name="testuser", email="test@test.com", password="password"
    )


@pytest.fixture
def test_users():
    user1 = User.objects.create_user(
        name="test1", email="test1@test.com", password="password"
    )
    user2 = User.objects.create_user(
        name="test2", email="test2@test.com", password="password"
    )

    return user1, user2


@pytest.mark.django_db
def test_sign_up(api_client):
    # 新規登録のエンドポイントにリクエスト
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "passwordtest",
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")

    # ステータスコードと期待されるユーザーが作成されたかを確認
    assert response.status_code == 201
    created_user = User.objects.get(email=input_data["email"])
    assert created_user.name == input_data["name"]


@pytest.mark.django_db
def test_sign_up_with_missing_name(api_client):
    input_data = {
        "name": None,
        "email": "test@test.com",
        "password": "passwordtest",
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")

    # ステータスコード確認
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_with_missing_email(api_client):
    input_data = {
        "name": "testuser",
        "email": None,
        "password": "passwordtest",
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")

    # ステータスコード確認
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_with_missing_password(api_client):
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": None,
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")

    # ステータスコード確認
    assert response.status_code == 400


@pytest.mark.django_db
def test_fetch_user_list_authenticated(api_client, test_users):
    api_client.force_authenticate(user=test_users[0])
    response = api_client.get(reverse("accounts:user_list"))
    assert response.status_code == 200
    assert response.data == UserListSerializer(test_users, many=True).data


@pytest.mark.django_db
def test_fetch_user_list_unauthenticated(api_client):
    response = api_client.get(reverse("accounts:user_list"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_fetch_user_detail_authenticated(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get(
        reverse("accounts:user_detail", kwargs={"pk": test_user.id})
    )
    assert response.status_code == 200
    assert response.data == UserRetrieveSerializer(test_user).data


@pytest.mark.django_db
def test_fetch_user_detail_unauthenticated(api_client, test_user):
    response = api_client.get(
        reverse("accounts:user_detail", kwargs={"pk": test_user.id})
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_fetch_user_detail_not_found(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get(
        reverse("accounts:user_detail", kwargs={"pk": test_user.id + 1})
    )
    assert response.status_code == 404
