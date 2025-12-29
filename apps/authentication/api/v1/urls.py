from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "auth_v1"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
    path(
        "logout/",
        TokenBlacklistView.as_view(),
        name="logout",
    ),
]
