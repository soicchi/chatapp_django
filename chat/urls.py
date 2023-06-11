from django.urls import include, path
from rest_framework import routers

from .views import RoomViewSet

router = routers.SimpleRouter()
router.register("rooms", RoomViewSet, basename="rooms")


urlpatterns = [
    path("", include(router.urls)),
]
