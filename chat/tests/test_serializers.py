import pytest
from django.contrib.auth import get_user_model

from chat.serializers import CreateRoomSerializer

BLANK_NAME_ERROR_MESSAGE = "チャットルーム名が空です"


@pytest.fixture
def test_user():
    User = get_user_model()
    user = User.objects.create_user(
        name="test_user", email="test@test.com", password="password"
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
