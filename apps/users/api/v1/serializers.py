from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserSerializer(ModelSerializer):
    """Full user serializer with all fields."""

    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "full_name",
            "last_active_at",
            "is_active",
            "is_staff",
        ]

    def to_representation(self, instance):
        """Remove uuid from representation since User uses 'id' as primary key."""
        data = super().to_representation(instance)
        data.pop("uuid", None)
        return data


class UserCreateSerializer(ModelSerializer):
    """Serializer for creating users."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields do not match."}
            )
        return attrs


class UserUpdateSerializer(ModelSerializer):
    """Serializer for updating users."""

    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "is_active",
            "is_staff",
        ]


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "full_name",
            "is_active",
            "created_by",
            "updated_by",
        ]
