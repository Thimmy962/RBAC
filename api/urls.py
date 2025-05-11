from django.urls import path
from . import views
from .utils import manageusers
urlpatterns = [
    path("users/", manageusers.list_create_staff, name="list_create_staff"),
    path("user/<int:pk>", manageusers.retrieve_update_destroy_staff, name = "retrieve_update_destroy_staff"),
    path("groups/", views.list_create_role, name = "list_create_role"),
    path("group/<int:pk>", views.retrieve_update_destroy_role, name = "retrieve_update_destroy_role")

]
