from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    ADMIN = "admin", _("Admin")
    USER = "user", _("User")
