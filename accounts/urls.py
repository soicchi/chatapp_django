from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import SignUpAPIView

app_name = "accounts"
urlpatterns = [
    path("signup/", SignUpAPIView.as_view()),
]
