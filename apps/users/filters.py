import django_filters

from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr="icontains")
    phone = django_filters.CharFilter(lookup_expr="icontains")

    ordering = django_filters.OrderingFilter(
        fields=(
            ("email", "email"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        )
    )

    class Meta:
        model = User
        fields = {
            "is_active": ["exact"],
            "is_staff": ["exact"],
            "created_by": ["exact"],
        }
