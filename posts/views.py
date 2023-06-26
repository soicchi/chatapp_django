from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostCreateSerializer


class PostViewSet(viewsets.ModelViewSet):
    """PostモデルのCRUDをまとめたクラス"""

    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.Serializer:
        if self.action == "create":
            return PostCreateSerializer
