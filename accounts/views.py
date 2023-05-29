from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import SignUpSerializer


class SignUpAPIView(generics.CreateAPIView):
    """新規登録のAPIクラス"""

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
