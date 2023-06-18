from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """ユーザーに関する各メソッドを管理するクラス"""

    def create_user(self, name: str, email: str, password: str) -> "CustomUser":
        # 各必須の値が与えられているかチェック
        if not name:
            raise ValueError("ユーザー名を入力してください")
        elif not email:
            raise ValueError("メールアドレスを入力してください")
        elif not password:
            raise ValueError("パスワードを入力してください")

        email = self.normalize_email(email)
        new_user = self.model(name=name, email=email)
        new_user.password = make_password(password)
        new_user.save(using=self._db)

        return new_user

    def create_superuser(
        self, name: str, email: str, password: str, **extra_fields
    ) -> "CustomUser":
        new_superuser = self.create_user(name, email, password)

        # スーパーユーザー用に値をセット
        new_superuser.is_staff = True
        new_superuser.is_superuser = True
        new_superuser.save(using=self._db)

        return new_superuser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ユーザーの認証モデル"""

    name = models.CharField(
        verbose_name="ユーザー名", max_length=255, blank=False, null=False
    )
    email = models.EmailField(
        verbose_name="メールアドレス", max_length=255, unique=True, blank=False, null=False
    )
    password = models.CharField(verbose_name="パスワード", max_length=255)
    last_login = models.DateTimeField(verbose_name="最終ログイン", blank=True, null=True)
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

    @classmethod
    def fetch_user(cls, user_id: int) -> "CustomUser":
        user = cls.objects.filter(pk=user_id).first()
        if not user:
            raise ValueError("指定されたユーザーIDのユーザーは存在しません")

        return user
