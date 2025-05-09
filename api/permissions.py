from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny


"""
Permissions to manage user
"""
class CustomAdminUser(BasePermission):
     def has_permission(self, request, view):
          user = request.user
          return bool(user and user.is_authenticated and user.is_staff and user.is_active)
     


class ManageEveryModelPermission(BasePermission):
    """
        This permission checks if: user is an active staff and has the permission to do what it is doing
        Gets the model and the api that contains the model
        Gets the corresponding perm for the request method from the perms_map
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
        # check if the user is an admin
        admin_check = CustomAdminUser().has_permission(request, view)
        if not admin_check:
            return False
        
        user = request.user

        # get model being worked on
        model = getattr(getattr(view, 'queryset', None), 'model', None)
        if not model:
            return False
        
        # get the api under which the model is
        app_label = model._meta.app_label

        # get the model namem
        model_name = model._meta.model_name

        # Cstom Super-permission: model_name_full_access
        # Was created for each model while defining each model
        full_access_perm = f"{app_label}.{model_name}_full_access"

        
        if request.user.has_perm(full_access_perm):
            return True

        # what permission is required for this request method
        # each request method is mapped to its corresponding perm in the perms_map variable above
        required_perm = self.perms_map.get(request.method)
        if not required_perm:
            return False
        
        # if the current user have the permission for this request method for this model
        # for instance, does this user have the add perm which correspond with the post request method for user model 
        specific_perm = f"{app_label}.{required_perm}_{model_name}"
        return user.has_perm(specific_perm)


class AllModelsPermissionMixin:
    permission_classes = [ManageEveryModelPermission]
