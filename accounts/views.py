from rest_framework import generics, serializers, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser
from .serializers import (
    SignUpSerializer,
    UserDestroySerializer,
    UserListSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)


class SignUpAPIView(generics.CreateAPIView):
    """新規登録のAPIクラス"""

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ユーザーモデルのAPIクラス"""

    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.Serializer:
        if self.action == "list":
            return UserListSerializer
        elif self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action == "partial_update":
            return UserUpdateSerializer
        elif self.action == "destroy":
            return UserDestroySerializer
        else:
            return super().get_serializer_class()
