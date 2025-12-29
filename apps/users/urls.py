from django.urls import include, path

from common.constants import API_V1

app_name = f"user_{API_V1}"

urlpatterns = [
    path(f"api/{API_V1}/users/", include("apps.users.api.v1.urls", namespace=app_name)),
]
