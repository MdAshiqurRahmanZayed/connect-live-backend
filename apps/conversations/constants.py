from django.db import models
from django.utils.translation import gettext_lazy as _


class ConversationType(models.TextChoices):
    DIRECT = "direct", _("Direct")
    GROUP = "group", _("Group")


class MembershipRole(models.TextChoices):
    OWNER = "owner", _("Owner")
    ADMIN = "admin", _("Admin")
    MODERATOR = "moderator", _("Moderator")
    MEMBER = "member", _("Member")


class RequestStatus(models.TextChoices):
    ACCEPTED = "accepted", _("Accepted")
    PENDING = "pending", _("Pending")
    REJECTED = "rejected", _("Rejected")
    BLOCKED = "blocked", _("Blocked")


DEFAULT_PINNED_MESSAGES_LIMIT = 50
DEFAULT_MAX_MEMBERS = 100
