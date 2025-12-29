from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.api.v1 import views

app_name = "user_api"
router = DefaultRouter()
router.register("users", views.UserApi, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
