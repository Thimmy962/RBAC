from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny


"""
Permissions to manage user
"""
class CustomAdminUser(BasePermission):
     def has_permission(self, request, view):
          user = request.user
          return bool(user and user.is_authenticated and user.is_staff and user.is_active)
     

class ManageUserPermission(BasePermission):
    def has_permission(self, request, view):
        admin_check = CustomAdminUser().has_permission(request, view)
        if not admin_check:
            return False

        user = request.user
        if user.has_perm("api.can_manage_user"):
            return True

        perms = [
            "api.add_user",
            "api.change_user",
            "api.delete_user",
            "api.view_user",
        ]
        return all(user.has_perm(p) for p in perms)



class ManageUserPermissionMixin:
    permission_classes = [ManageUserPermission]




"""
Permissions to manage roles/groups and custom permissions
"""

class ManageRolesPermissions(BasePermission):
    def has_permission(self, request, view):
        perms = [
                "api.add_user",
                "api.change_user",
                "api.delete_user",
                "api.view_user",
            ]
        return all(request.user.has_perm(p) for p in perms)
    
class ManageRolesPermissionsMixin:
    permision_classes = [ManageRolesPermissions]
        


