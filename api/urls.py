from django.urls import path
from api import views
from api.utils import manageusers
urlpatterns = [
    path("users/", manageusers.list_create_staff, name="list_create_staff"),
    path("user/<int:pk>", manageusers.retrieve_update_destroy_staff, name = "retrieve_update_destroy_staff"),
    path("groups/", views.list_create_role, name = "list_create_role"),
    path("group/<int:pk>", views.retrieve_role, name = "retrieve_role"),
    path("genres/", views.list_create_genre, name = "list_create_genre"),
    path("genre/<int:pk>", views.retrieve_update_destroy_genre, name = "retrieve_update_destroy_genre")

]
