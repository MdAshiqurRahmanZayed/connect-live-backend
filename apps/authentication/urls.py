from django.urls import include, path

from common.constants import API_V1

app_name = f"auth{API_V1}"

urlpatterns = [
    path(
        f"api/{API_V1}/auth/",
        include(("apps.authentication.api.v1.urls", "auth"), namespace=app_name),
    ),
]
