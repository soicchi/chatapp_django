from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser
from .serializers import SignUpSerializer, UserListSerializer, UserRetrieveSerializer


class SignUpAPIView(generics.CreateAPIView):
    """新規登録のAPIクラス"""

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class UserListAPIView(generics.ListAPIView):
    """ユーザー一覧を返すAPIクラス"""

    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ユーザー詳細を返すAPIクラス"""

    queryset = CustomUser.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]
