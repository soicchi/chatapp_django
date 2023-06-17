from rest_framework import serializers, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Room, RoomMember
from .serializers import CreateRoomSerializer, LeaveRoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """RoomモデルのCRUDをまとめたクラス"""

    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.Serializer:
        if self.action == "create":
            return CreateRoomSerializer


class LeaveRoomAPIView(views.APIView):
    """チャットルームを退出するクラス"""

    queryset = Room.objects.all()
    serializer_class = LeaveRoomSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = LeaveRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.destroy(serializer.validated_data)
        except ValueError as e:
            return Response({
                "message": str(e),
            }, status=400)

        return Response({
            "message": "チャットルームを退出しました",
        }, status=204)
