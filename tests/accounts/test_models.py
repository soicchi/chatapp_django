import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    name = "testuser"
    email = "test@test.com"
    password = "testpassword"

    # 作成が成功の場合
    new_user = User.objects.create_user(name, email, password)
    assert new_user.name == name
    assert new_user.email == email
    assert new_user.check_password(password)
    assert new_user.is_staff == False
    assert new_user.is_superuser == False

    # nameがない場合
    with pytest.raises(ValueError, match="The given name must be set"):
        User.objects.create_user(None, email, password)

    # emailがない場合
    with pytest.raises(ValueError, match="The given email must be set"):
        User.objects.create_user(name, None, password)

    # passwordがない場合
    with pytest.raises(ValueError, match="The given password must be set"):
        User.objects.create_user(name, email, None)


@pytest.mark.django_db
def test_create_superuser():
    name = "testuser"
    email = "test@test.com"
    password = "testpassword"

    # スーパーユーザー作成が成功した場合
    new_superuser = User.objects.create_superuser(name, email, password)
    assert new_superuser.name == name
    assert new_superuser.email == email
    assert new_superuser.check_password(password)
    assert new_superuser.is_staff == True
    assert new_superuser.is_superuser == True
