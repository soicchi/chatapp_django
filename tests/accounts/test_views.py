import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
base_url = "/api/v1"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_sign_up(api_client):
    # 新規登録のエンドポイントにリクエスト
    signup_url = f"{base_url}/signup/"
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": "passwordtest",
    }
    response = api_client.post(signup_url, input_data, format="json")

    # ステータスコードと期待されるユーザーが作成されたかを確認
    assert response.status_code == 201
    created_user = User.objects.get(email=input_data["email"])
    assert created_user.name == input_data["name"]


@pytest.mark.django_db
def test_sign_up_with_missing_name(api_client):
    signup_url = f"{base_url}/signup/"
    input_data = {
        "name": None,
        "email": "test@test.com",
        "password": "passwordtest",
    }
    response = api_client.post(signup_url, input_data, format="json")

    # ステータスコード確認
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_with_missing_email(api_client):
    signup_url = f"{base_url}/signup/"
    input_data = {
        "name": "testuser",
        "email": None,
        "password": "passwordtest",
    }
    response = api_client.post(signup_url, input_data, format="json")

    # ステータスコード確認
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_with_missing_password(api_client):
    signup_url = f"{base_url}/signup/"
    input_data = {
        "name": "testuser",
        "email": "test@test.com",
        "password": None,
    }
    response = api_client.post(signup_url, input_data, format="json")

    # ステータスコード確認
    assert response.status_code == 400
