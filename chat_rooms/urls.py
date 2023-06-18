from django.urls import include, path
from rest_framework import routers

from .views import JoinRoomAPIView, LeaveRoomAPIView, RoomViewSet

router = routers.SimpleRouter()
router.register("rooms", RoomViewSet, basename="rooms")


app_name = "chat_rooms"
urlpatterns = [
    path("", include(router.urls)),
    path("join/", JoinRoomAPIView.as_view(), name="join_room"),
    path("leave/", LeaveRoomAPIView.as_view(), name="leave_room"),
]
