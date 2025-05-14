from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# staff model
class Staff(AbstractUser):
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

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return perm in self.get_group_permissions(obj)

    def has_perms(self, perm_list, obj=None):
        if self.is_superuser:
            return True
        return all(self.has_perm(perm, obj) for perm in perm_list)
    
    class Meta:
        permissions = [
            ("staff_full_access", "Staff Full Access")
        ]
        ordering = ['username']


# genre model
class Genre(models.Model):
    genre = models.CharField(max_length=32, unique=True)

    class Meta:
        permissions = [
            ("genre_full_access", "Genre Full Access")
        ]
        ordering = ['genre']

    def __str__(self):
        return self.genre



# author model
class Author(models.Model):
    first_name = models.CharField(max_length = 32, unique = True, editable = True, blank = False, null = False)
    last_name = models.CharField(max_length = 32, unique = True, editable = True, blank = False, null = False)

    def name(self):
        return f"{self.last_name} {self.first}"
    
    class Meta:
        permissions = [
            ("author_full_access", "Author Full Access")
        ]
        ordering = ['first_name', 'last_name']


class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key = True, auto_created = True)
    title = models.CharField(max_length = 256, blank = False, null = False)
    author = models.ManyToManyField(Author, related_name = "author_books", blank = True)
    genre = models.ManyToManyField(Genre, related_name = "genre_books", blank = True)
    ISBN = models.CharField(max_length = 24, blank=True)


    class Meta:
        permissions = [
            ("booK_full_access", "BooK_Full_Access")
        ]
