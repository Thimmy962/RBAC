from functools import wraps
from graphql import GraphQLError  # Optional: for better GraphQL-specific errors
from rest_framework.permissions import BasePermission

SAFE_METHODS = ("GET", "OPTIONS", "HEAD")

class CustomAdminUser(BasePermission):
    """
    Grants access only to authenticated, active, staff users.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff and user.is_active)


class ManageEveryModelPermission(BasePermission):
    """
    Grants access to specific model actions based on:
    - Active staff check
    - Superuser override
    - Full-access permission (model_name_full_access)
    - Mapped permission for request method (add, change, delete, view)
    """
    perms_map = {
        'GET': 'view',
        'OPTIONS': 'view',
        'HEAD': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete',
    }

    def has_permission(self, request, view):
        user = request.user

        # Admin pre-check
        if not CustomAdminUser().has_permission(request, view):
            return False

        if user.is_superuser:
            return True

        model = getattr(getattr(view, 'queryset', None), 'model', None)
        if model is None:
            return False  # You may want to log this for debugging

        app_label = model._meta.app_label
        model_name = model._meta.model_name

        # Check full-access permission
        full_access_perm = f"{app_label}.{model_name}_full_access"
        if user.has_perm(full_access_perm):
            return True

        # Map HTTP method to Django permission type
        perm_action = self.perms_map.get(request.method)
        if perm_action is None:
            return False

        specific_perm = f"{app_label}.{perm_action}_{model_name}"
        return user.has_perm(specific_perm)



class AllModelsPermissionMixin:
    permission_classes = [ManageEveryModelPermission]



def permissions_decorator(model_class):
    def decorator(func):
        @wraps(func)
        def wrapper(self, info, *args, **kwargs):
            user = info.context.user

            if not (user and user.is_authenticated and user.is_active and user.is_staff):
                raise GraphQLError(
                    message="Authentication required: user must be active staff.",
                    extensions={
                        "code": "AUTH_REQUIRED",
                        "reason": "Inactive or unauthenticated staff user",
                        "http_status": 401
                    }
                )

            if user.is_superuser:
                return func(self, info, *args, **kwargs)

            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name

            required_perms = [
                f"{app_label}.{model_name}_full_access",
                f"{app_label}.view_{model_name}",
            ]

            if any(user.has_perm(perm) for perm in required_perms):
                return func(self, info, *args, **kwargs)

            raise GraphQLError(
                message="Permission denied: insufficient access rights.",
                extensions={
                    "code": "PERMISSION_DENIED",
                    "model": model_name,
                    "app": app_label,
                    "required": required_perms,
                    "http_status": 403
                }
            )
        return wrapper
    return decorator
