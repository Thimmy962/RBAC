from django.urls import path
from api import views, schema
from api.utils import manageusers
from graphene_django.views import GraphQLView



urlpatterns = [
    path("users/", manageusers.create_staff, name="create_staff"),
    path("user/<int:pk>", manageusers.update_destroy_staff, name = "update_destroy_staff"),
    path("groups/", views.create_role, name = "create_role"),
    path("group/<int:pk>", views.update_destroy_role, name = "update_destroy_role"),
    path("genres/", views.create_genre, name = "create_genre"),
    path("genre/<int:pk>", views.update_destroy_genre, name = "update_destroy_genre"),
    path("authors/", views.create_author, name = "create_author"),
    path("author/<int:pk>", views.update_destroy_author, name = "update_destroy_author"),
    path("books/", views.create_book, name = "create_book"),
    path("book/<str:pk>", views.update_destroy_book, name = "update_destroy_book"),
]
