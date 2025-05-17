from django.urls import path
from api import views
from api.utils import manageusers
urlpatterns = [
    path("users/", manageusers.list_create_staff, name="list_create_staff"),
    path("user/<int:pk>", manageusers.retrieve_update_destroy_staff, name = "retrieve_update_destroy_staff"),
    path("groups/", views.list_create_role, name = "list_create_role"),
    path("group/<int:pk>", views.retrieve_update_destroy_role, name = "retrieve_update_destroy_role"),
    path("genres/", views.list_create_genre, name = "list_create_genre"),
    path("genre/<int:pk>", views.retrieve_update_destroy_genre, name = "retrieve_update_destroy_genre"),
    path("authors/", views.list_create_author, name = "list_create_author"),
    path("author/<int:pk>", views.retrieve_update_destroy_author, name = "retrieve_update_destroy_author"),
    path("books/", views.list_create_book, name = "list_create_book"),
    path("book/<str:pk>", views.retrieve_update_destroy_book, name = "retrieve_update_destroy_book"),

]
