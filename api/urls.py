from django.urls import path
from . import views
from .utils import manageusers
urlpatterns = [
    path("", views.index),
    path("users/", manageusers.list_Create_user, name="register")
]
