from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from api.tasks import cache_staffs_permission_on_grp_perm_change, cache_a_staff_group_perms
from django.contrib.auth import get_user_model

Staff = get_user_model()



@receiver(m2m_changed, sender=Group.permissions.through)
def update_users_perms_in_a_grp(sender, instance, action, **kwargs):
    """
        If there is a change in the permissions of a group
        Call the "cache_staffs_permission_on_grp_perm_change" background task function to cache the accumulated grp permissions 
            of all the staffs in that group.
    """
    if action in ('post_add', 'post_remove', 'post_clear'):
       cache_staffs_permission_on_grp_perm_change.delay(instance.id)



@receiver(m2m_changed, sender=Staff.groups.through)
def update_user_perms_on_grp_change(sender, instance, action, **kwargs):
    """
        If there is any change in the grp of this user
        Call the "cache_a_staff_group_perms" background task fucntion to cache the accumulated grp permissions to the user id
    """
    if action in ('post_add', 'post_remove', 'post_clear'):
       cache_a_staff_group_perms.delay(instance.id)
