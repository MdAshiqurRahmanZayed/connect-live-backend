from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from apps.conversations.constants import (
    DEFAULT_MAX_MEMBERS,
    DEFAULT_PINNED_MESSAGES_LIMIT,
    ConversationType,
    MembershipRole,
    RequestStatus,
)
from apps.users.models.users import User
from common.models import BaseModel


class Conversation(BaseModel):
    conversation_type = models.CharField(
        max_length=20, choices=ConversationType.choices
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="conversations/", null=True, blank=True)
    members = models.ManyToManyField(
        User,
        through="ConversationMembership",
        through_fields=("conversation", "user"),
        related_name="members_conversation",
    )
    is_archived = models.BooleanField(default=False)
    last_message_at = models.DateTimeField(null=True, blank=True)
    pinned_messages_limit = models.IntegerField(default=DEFAULT_PINNED_MESSAGES_LIMIT)

    max_members = models.IntegerField(
        default=DEFAULT_MAX_MEMBERS, null=True, blank=True
    )
    is_private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.conversation_type == ConversationType.DIRECT and not self.title:
            self.title = "Direct Message"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.conversation_type == ConversationType.DIRECT:
            return f"Direct: {self.uuid}"
        return f"Group: {self.title} Members: {self.members.count()}"


class ConversationMembership(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_conversation_memberships"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="conversation_conversation_memberships",
    )
    role = models.CharField(
        max_length=20, choices=MembershipRole.choices, default=MembershipRole.MEMBER
    )
    request_status = models.CharField(
        max_length=20, choices=RequestStatus.choices, default=RequestStatus.ACCEPTED
    )
    request_message = models.TextField(blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    notification_enabled = models.BooleanField(default=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Conversion Membership"
        verbose_name_plural = "Conversion Memberships"
        constraints = [
            UniqueConstraint(
                fields=["user", "conversation"], name="unique_user_conversation"
            ),
        ]

    def clean(self):
        # Direct conversations should have exactly 2 members
        if self.conversation.conversation_type == ConversationType.DIRECT:
            current_members = (
                self.conversation.conversation_conversation_memberships.filter(
                    request_status=RequestStatus.ACCEPTED
                ).count()
            )
            if current_members >= 2 and self.pk is None:
                raise ValidationError("Direct conversations can only have 2 members")

            # In direct conversations, only 'member' role is allowed
            if self.role != MembershipRole.MEMBER:
                raise ValidationError("Direct conversations only support 'member' role")

    def __str__(self):
        return f"{self.user} in {self.conversation.title} ({self.role})"
