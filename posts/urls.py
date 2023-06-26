from django.urls import include, path
from rest_framework import routers

from .views import PostViewSet

router = routers.SimpleRouter()
router.register("posts", PostViewSet, basename="posts")


app_name = "posts"
urlpatterns = [
    path("", include(router.urls)),
]