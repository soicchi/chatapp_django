from .models import CustomUser


class UserManagerService:
    """CustomUserの作成、削除、更新などの基本的な操作を行うクラス"""

    def __init__(self, user_model=CustomUser) -> None:
        self.user_model = user_model

    def create_user(self, name: str, email: str, password: str) -> CustomUser:
        new_user = self.user_model.objects.create_user(
            name=name,
            email=email,
            password=password,
        )

        return new_user
