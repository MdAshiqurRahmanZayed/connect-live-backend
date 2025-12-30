from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from apps.conversations.models.conversation import Conversation, ConversationMembership


class ConversationMembershipInline(admin.TabularInline):
    model = ConversationMembership
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = (
        "user",
        "role",
        "request_status",
        "is_blocked",
        "notification_enabled",
        "nickname",
        "created_at",
    )
    autocomplete_fields = ["user"]


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "title",
        "conversation_type",
        "member_count",
        "is_private",
        "is_archived",
    )
    list_filter = ("conversation_type",)
    search_fields = ("title", "description", "uuid")
    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
        "avatar_preview",
    )
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "conversation_type",
                    "title",
                    "description",
                    "avatar",
                    "avatar_preview",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "is_private",
                    "is_archived",
                    "max_members",
                    "pinned_messages_limit",
                )
            },
        ),
        (
            "Activity",
            {"fields": ("last_message_at",)},
        ),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (
                "Basic Information",
                {
                    "fields": (
                        "conversation_type",
                        "title",
                        "description",
                        "avatar",
                    )
                },
            ),
            (
                "Settings",
                {
                    "fields": (
                        "is_private",
                        "is_archived",
                        "max_members",
                        "pinned_messages_limit",
                    )
                },
            ),
            (
                "Activity",
                {"fields": ("last_message_at",)},
            ),
        ]

        # Add avatar_preview and timestamps only when editing existing object
        if obj:
            fieldsets[0][1]["fields"] = (
                "conversation_type",
                "title",
                "description",
                "avatar",
                "avatar_preview",
            )
            fieldsets.append(
                (
                    "Timestamps",
                    {
                        "fields": ("uuid", "created_at", "updated_at"),
                        "classes": ("collapse",),
                    },
                )
            )

        return fieldsets

    inlines = [ConversationMembershipInline]
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(member_count=Count("members"))
        return queryset

    def member_count(self, obj):
        return obj.member_count

    member_count.short_description = "Members"
    member_count.admin_order_field = "member_count"

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; border-radius: 8px;" />',
                obj.avatar.url,
            )
        return format_html('<span style="color: #999;">No avatar</span>')

    avatar_preview.short_description = "Avatar Preview"


@admin.register(ConversationMembership)
class ConversationMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "user",
        "conversation_title",
        "role",
        "request_status",
        "is_blocked",
        "notification_enabled",
    )
    list_filter = (
        "role",
        "request_status",
        "is_blocked",
        "notification_enabled",
    )
    search_fields = (
        "user__username",
        "user__email",
        "conversation__title",
        "nickname",
    )
    readonly_fields = ("uuid", "created_at", "updated_at", "conversation_type")
    autocomplete_fields = ["user", "conversation"]
    fieldsets = (
        (
            "Membership Information",
            {
                "fields": (
                    "user",
                    "conversation",
                    "nickname",
                )
            },
        ),
        (
            "Role & Status",
            {
                "fields": (
                    "role",
                    "request_status",
                    "request_message",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "is_blocked",
                    "notification_enabled",
                )
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (
                "Membership Information",
                {
                    "fields": (
                        "user",
                        "conversation",
                        "nickname",
                    )
                },
            ),
            (
                "Role & Status",
                {
                    "fields": (
                        "role",
                        "request_status",
                        "request_message",
                    )
                },
            ),
            (
                "Settings",
                {
                    "fields": (
                        "is_blocked",
                        "notification_enabled",
                    )
                },
            ),
        ]

        # Add uuid, conversation_type, and timestamps only when editing existing object
        if obj:
            fieldsets[0][1]["fields"] = (
                "uuid",
                "user",
                "conversation",
                "conversation_type",
                "nickname",
            )
            fieldsets.append(
                (
                    "Timestamps",
                    {
                        "fields": ("created_at", "updated_at"),
                        "classes": ("collapse",),
                    },
                )
            )

        return fieldsets

    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def conversation_title(self, obj):
        return obj.conversation.title

    conversation_title.short_description = "Conversation"
    conversation_title.admin_order_field = "conversation__title"

    def conversation_type(self, obj):
        type_colors = {
            "direct": "#28a745",
            "group": "#007bff",
            "channel": "#ffc107",
        }
        color = type_colors.get(obj.conversation.conversation_type, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.conversation.conversation_type.upper(),
        )

    conversation_type.short_description = "Type"
