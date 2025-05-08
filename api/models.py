from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# staff model
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
    
    class Meta:
        permissions = [
            ("staff_full_access", "Staff full Access")
        ]


# genre model
class Genre(models.Model):
    genre = models.CharField(max_length = 32, unique = True, editable = True)

    class Meta:
        permissions = [
            ("genre_full_access", "Genre Full Access")
        ]


# author model
class Author(models.Model):
    first_name = models.CharField(max_length = 32, unique = True, editable = True, blank = False, null = False)
    last_name = models.CharField(max_length = 32, unique = True, editable = True, blank = False, null = False)

    class Meta:
        permissions = [
            ("author_full_access", "author full Access")
        ]
