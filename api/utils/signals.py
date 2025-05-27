import threading
from django.db.models.signals import pre_delete
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core.cache import cache

_thread_local = threading.local()

# @receiver(m2m_changed, sender=Group.permissions.through)
# def update_group_permission_cache(sender, instance, action, **kwargs):

#     if action == 'post_add':
#         perms = instance.permissions.all()
#         print(perms)
#         perm_list = [perm.codename for perm in perms]
#         cache.set(instance.name, perm_list, timeout=None)
#     elif action == 'post_clear':
#         # permissions have been cleared manually or via .set([])
#         cache.delete(instance.name)

# delete cache for this grp if the grp is deleted
@receiver(pre_delete, sender=Group)
def clear_group_cache_on_delete(sender, instance, **kwargs):
    cache.delete(instance.name)




@receiver(m2m_changed, sender=Group.permissions.through)
def update_group_permission_cache(sender, instance, action, **kwargs):
    print("Caching")
    if action == 'pre_clear':
        # Mark this thread as doing a set operation
        _thread_local.in_set_operation = True


    elif action == 'post_clear':
        # Only clear the cache if no add is coming after
        if not getattr(_thread_local, 'in_set_operation', False):
            cache.delete(instance.name)

    elif action == 'post_add':
        perms = instance.permissions.all()
        perm_list = [perm.codename for perm in perms]
        cache.set(instance.name, perm_list, timeout=None)
        # Clear the flag after caching
        _thread_local.in_set_operation = False