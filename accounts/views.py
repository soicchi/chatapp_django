from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser
from .serializers import SignUpSerializer, UserListSerializer


class SignUpAPIView(generics.CreateAPIView):
    """新規登録のAPIクラス"""

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class UserListAPIView(generics.ListAPIView):
    """ユーザー一覧を返すAPIクラス"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = CustomUser.objects.all()
