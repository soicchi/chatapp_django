from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import SignUpAPIView, UserViewSet

router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="users")

app_name = "accounts"
urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
