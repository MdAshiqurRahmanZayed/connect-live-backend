from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication


class BaseModelViewSet(ModelViewSet):
    """
    Custom ModelViewSet with soft delete, hard delete, and automatic user tracking.

    Features:
    - Action-based permission classes and serializers
    - Automatic tracking of created_by, updated_by, and deleted_by fields
    - Soft delete functionality (marks records as deleted without removing from database)
    - Hard delete option for permanent removal with user tracking

    Assumptions:
        Your model should inherit from a base model that includes:
        - created_by (ForeignKey to User, optional)
        - updated_by (ForeignKey to User, optional)
        - deleted_by (ForeignKey to User, optional)
        - is_deleted (BooleanField)
        - deleted_at (DateTimeField, optional)

    Usage:
        Define permission_classes_by_action and serializer_classes_by_action
        dictionaries in your subclass to customize behavior per action.

    Example:
        class MyViewSet(BaseModelViewSet):
            permission_classes_by_action = {
                'list': [IsAuthenticated],
                'create': [IsAdminUser],
            }
            serializer_classes_by_action = {
                'list': ListSerializer,
                'create': CreateSerializer,
            }
    """

    permission_classes_by_action = {}
    serializer_classes_by_action = {}

    def get_permissions(self):
        permission_classes = self.permission_classes_by_action.get(
            self.action, self.permission_classes
        )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(
            self.action, super().get_serializer_class()
        )

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(updated_by=self.request.user)
        else:
            serializer.save()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()

        if self.request.user.is_authenticated:
            instance.deleted_by = self.request.user
            instance.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])
        else:
            instance.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, instance):
        if self.request.user.is_authenticated:
            instance.deleted_by = self.request.user
            instance.deleted_at = timezone.now()
            instance.save(update_fields=["deleted_by", "deleted_at"])

        instance.delete()


class CsrfExemptedSessionAuthentication(SessionAuthentication):
    """
    DRF SessionAuthentication is enforcing CSRF, which may be problematic.
    That's why we want to make sure we are exempting any kind of CSRF checks for APIs.
    """

    def enforce_csrf(self, request):
        return


class ApiAuthMixin:
    """
    Mixin to enforce API authentication and permissions for DRF views.

    Current behavior:
    - Uses JWTAuthentication for authenticating users.
    - Requires that users are authenticated (IsAuthenticated permission).

    Purpose:
    - Centralizes authentication and permission logic for reuse across multiple views.
    - Ensures consistent security standards across the API.

    Future extensions:
    - Can be extended to support multiple authentication schemes.
    - Can include custom permissions for role-based access control.
    """

    authentication_classes = [JWTAuthentication, CsrfExemptedSessionAuthentication]
    permission_classes = [IsAuthenticated]
