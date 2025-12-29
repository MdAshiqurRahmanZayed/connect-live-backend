from rest_framework.permissions import AllowAny, IsAdminUser

from apps.users.api.v1.serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.users.filters import UserFilter
from apps.users.models import User
from common.mixins import ApiAuthMixin, BaseModelViewSet


class UserApi(ApiAuthMixin, BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [AllowAny]

    permission_classes_by_action = {
        "destroy": [IsAdminUser],
    }

    serializer_classes_by_action = {
        "list": UserListSerializer,
        "create": UserCreateSerializer,
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer,
    }

    def perform_create(self, serializer):
        validated_data = serializer.validated_data.copy()
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        if self.request.user.is_authenticated:
            user.created_by = self.request.user
            user.save(update_fields=["created_by"])
