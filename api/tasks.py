from __future__ import absolute_import

from django.contrib.auth.models import Group
from django.core.cache import cache
from typing import List
from django.contrib.auth import get_user_model
from celery import shared_task




@shared_task
def cache_a_staff_group_perms(user_id):
    """
        Get all the grp_permissions for this user
            and cache them to this user
    """
    Staff = get_user_model()
    try:
        user = Staff.objects.prefetch_related('groups__permissions').get(id=user_id)
        perms = user.get_group_permissions()
        perms_list = set(perms)
        cache.set(f"{user_id}", perms_list)
    except Staff.DoesNotExist:
        pass  # optionally log this



@shared_task
def cache_staffs_permission_on_grp_perm_change(group_id):
    """
        Gets the users in this group and call the cache_a_staff_group_perms on each user
            to cache each users grp_permissions to the user id
    """
    try:
        group = Group.objects.prefetch_related('user_set__groups__permissions').get(id=group_id)
        all_grp_users = group.user_set.all()
        for user in all_grp_users:
            cache_a_staff_group_perms.delay(user.id)
    except Group.DoesNotExist:
        pass  # optionally log this



