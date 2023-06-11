from rest_framework import IsAuthenticated, serializers, viewsets

from .models import Room
from .serializers import CreateRoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """RoomモデルのCRUDをまとめたクラス"""

    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.Serializer:
        if self.action == "create":
            return CreateRoomSerializer
