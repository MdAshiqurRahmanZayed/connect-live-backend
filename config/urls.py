from decouple import config
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from common.constants import LOCAL_SERVER

schema_view = get_schema_view(
    openapi.Info(
        title="Connect Live",
        default_version="v1",
        description="Connect Live API DOC",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mdzayed2019@gmai.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("apps.users.urls")),
    path("", include("apps.authentication.urls")),
]

if config("SERVER_NAME") == LOCAL_SERVER:
    urlpatterns += [
        path(
            "swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
