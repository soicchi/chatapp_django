from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    SignUpAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = "accounts"
urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/<pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
]
