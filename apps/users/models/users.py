from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.constants import UserType
from apps.users.managers import UserManager
from common.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(
        verbose_name=_("Email Address"), db_column="email", unique=True, db_index=True
    )
    user_type = models.CharField(
        verbose_name=_("User Type"),
        max_length=25,
        choices=UserType.choices,
        null=False,
        blank=False,
        default=UserType.USER,
    )
    first_name = models.CharField(
        verbose_name=_("First Name"),
        db_column="first_name",
        max_length=254,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        verbose_name=_("Last Name"),
        db_column="last_name",
        max_length=254,
        blank=True,
        null=True,
    )

    last_active_at = models.DateTimeField(
        verbose_name="Last active at", blank=True, null=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"), db_index=True, default=False
    )
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"
