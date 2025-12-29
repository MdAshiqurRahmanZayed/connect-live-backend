from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "full_name",
        "user_type",
        "is_active",
    )

    list_filter = (
        "is_active",
        "user_type",
    )

    search_fields = ("email", "first_name", "last_name", "uuid")

    ordering = ("-created_at",)

    readonly_fields = (
        "uuid",
        "last_login",
        "last_active_at",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "deleted_at",
        "deleted_by",
    )

    fieldsets = (
        (
            _("Personal Info"),
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("User Classification"),
            {"fields": ("user_type",)},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Security"),
            {
                "fields": (
                    "password",
                    "last_login",
                    "last_active_at",
                )
            },
        ),
        (
            _("Tracking Info"),
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "created_by",
                    "updated_at",
                    "updated_by",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Deletion Info"),
            {
                "fields": (
                    "is_deleted",
                    "deleted_at",
                    "deleted_by",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            _("Personal Info"),
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("User Classification"),
            {"fields": ("user_type",)},
        ),
        (
            _("Security"),
            {
                "fields": (
                    "password1",
                    "password2",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")
