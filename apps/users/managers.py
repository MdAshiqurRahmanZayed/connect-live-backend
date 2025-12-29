from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

from common.models import IsDeletedManager


class UserManager(BaseUserManager, IsDeletedManager):
    use_in_migrations = True

    @transaction.atomic()
    def _create_user(self, email, password, **extra_fields):
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)
