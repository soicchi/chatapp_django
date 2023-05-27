from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """ユーザーに関する各メソッドを管理するクラス"""

    def create_user(self, name, email, password):
        # 各必須の値が与えられているかチェック
        if not name:
            raise ValueError("The given name must be set")
        elif not email:
            raise ValueError("The given email must be set")
        elif not password:
            raise ValueError("The given password must be set")

        email = self.normalize_email(email)
        new_user = self.model(name=name, email=email)
        new_user.password = make_password(password)
        new_user.save(using=self._db)

        return new_user

    def create_superuser(self, name, email, password, **extra_fields):
        new_superuser = self.create_user(name, email, password)

        # スーパーユーザー用に値をセット
        new_superuser.is_staff = True
        new_superuser.is_superuser = True
        new_superuser.save(using=self._db)

        return new_superuser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ユーザーの認証モデル"""

    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.email
