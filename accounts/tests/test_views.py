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
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "password",
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")
    assert response.status_code == 201

    # 期待されるユーザーが作成されたかを確認
    created_user = User.objects.get(email=input_data["email"])
    assert created_user.name == input_data["name"]


@pytest.mark.django_db
def test_sign_up_with_missing_name(api_client):
    input_data = {
        "name": None,
        "email": "test@test.com",
        "password": "password",
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_with_missing_email(api_client):
    input_data = {
        "name": "testuser",
        "email": None,
        "password": "password",
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_with_missing_password(api_client):
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": None,
    }
    response = api_client.post(reverse("accounts:signup"), input_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_fetch_user_list_authenticated(api_client, test_users):
    # test_users[0]で認証
    api_client.force_authenticate(user=test_users[0])
    response = api_client.get(reverse("accounts:user_list"))
    assert response.status_code == 200

    # レスポンスに含まれるユーザーリストが正しいか検証
    assert response.data == UserListSerializer(test_users, many=True).data


@pytest.mark.django_db
def test_fetch_user_list_unauthenticated(api_client):
    response = api_client.get(reverse("accounts:user_list"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_fetch_user_detail_authenticated(api_client, test_user):
    # test_userで認証
    api_client.force_authenticate(user=test_user)
    response = api_client.get(
        reverse("accounts:user_detail", kwargs={"pk": test_user.id})
    )
    assert response.status_code == 200

    # レスポンスに含まれるユーザーが正しいか検証
    assert response.data == UserRetrieveSerializer(test_user).data


@pytest.mark.django_db
def test_fetch_user_detail_unauthenticated(api_client, test_user):
    response = api_client.get(
        reverse("accounts:user_detail", kwargs={"pk": test_user.id})
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_fetch_user_detail_not_found(api_client, test_user):
    # test_userで認証
    api_client.force_authenticate(user=test_user)
    not_existed_user_id = test_user.id + 1
    response = api_client.get(
        reverse("accounts:user_detail", kwargs={"pk": not_existed_user_id})
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_user_authenticated(api_client, test_user):
    # test_userで認証
    api_client.force_authenticate(user=test_user)
    update_data = {
        "name": "updated_user",
        "email": "updated@test.com",
    }
    response = api_client.patch(
        reverse("accounts:user_update", kwargs={"pk": test_user.id}),
        data=update_data,
        format="json",
    )
    assert response.status_code == 200

    # DBを更新
    test_user.refresh_from_db()

    # 更新したユーザーデータが反映されているか検証
    assert test_user.name == update_data["name"]
    assert test_user.email == update_data["email"]


@pytest.mark.django_db
def test_update_user_unauthenticated(api_client, test_user):
    update_data = {
        "name": "updated_user",
        "email": "updated@test.com",
    }
    response = api_client.patch(
        reverse("accounts:user_update", kwargs={"pk": test_user.id}),
        data=update_data,
        format="json",
    )
    assert response.status_code == 401
