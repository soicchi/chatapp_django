from django.urls import path

from .views import SignUpAPIView


app_name = "accounts"
urlpatterns = [
    path("signup/", SignUpAPIView.as_view()),
]