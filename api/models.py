from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="user_groups",  # Custom related name for 'groups'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions",  # Custom related name for 'user_permissions'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # This is a custom save method to set the password if it is not already set
    def save(self, *args, **kwargs):
        if not self.pk and not self.check_password(self.password):
            self.set_password(self.password)
        return super().save(*args, **kwargs)


