from django.urls import include, path
from rest_framework import routers

from .views import LeaveRoomAPIView, RoomViewSet

router = routers.SimpleRouter()
router.register("rooms", RoomViewSet, basename="rooms")


app_name = "chat"
urlpatterns = [
    path("", include(router.urls)),
    path("leave/", LeaveRoomAPIView.as_view(), name="leave_room"),
]
