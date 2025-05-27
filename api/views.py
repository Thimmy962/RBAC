from rest_framework import status, response, generics
from api.utils import serializers
from django.contrib.auth.models import Group
from api.permissions import AllModelsPermissionMixin
from api.models import Author, Book, Genre
# Create your views here.


# TO CREATE OR LIST BOOK
class CreateBookView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    """
    def perform_create(self, serializer):
        ser = serializer.save()
        perform  logging here
    """

create_book = CreateBookView.as_view()

class UpdateDestroyBookView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    """
    def perform_update(self, serializer):
        ser = serializer.save()
        log activity
    
        
        def perform_destroy(self, instance):
            log before deleting
            instance.destroy()
    """
update_destroy_book = UpdateDestroyBookView.as_view()


# TO CREATE OR LIST AUTHOR
class CreateAuthorView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer

    """
    def perform_create(self, serializer):
        ser = serializer.save()
        perform  logging here
    """
create_author = CreateAuthorView.as_view()


# UPDATE OR DESTROY AUTHOR
class UpdateDestroyAuthorView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer

    """
    def perform_update(self, serializer):
        ser = serializer.save()
        log activity
    
        
        def perform_destroy(self, instance):
            log before deleting
            instance.destroy()
    """
update_destroy_author = UpdateDestroyAuthorView.as_view()

# TO CREATE GENRE
class CreateGenreView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer

    """
    def perform_create(self, serializer):
        ser = serializer.save()
        perform  logging here
    """
create_genre = CreateGenreView.as_view()


# UPDATE OR DESTROY GENRE
class UpdateDestroyGenreView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer

    """
    def perform_update(self, serializer):
        ser = serializer.save()
        log activity
    
        
        def perform_destroy(self, instance):
            log before deleting
            instance.destroy()
    """
update_destroy_genre = UpdateDestroyGenreView.as_view()


# TO CREATE ROLE
class CreateRoleView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.CreateRoleSerializer

    """
    def perform_create(self, serializer):
        ser = serializer.save()
        perform  logging here
    """
create_role = CreateRoleView.as_view()


# UPDATE OR DESTROY ROLE
class UpdateDestroyRoleView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.UpdateDestroyRoleSerializer

    """
    def perform_update(self, serializer):
        ser = serializer.save()
        log activity
    
        
        def perform_destroy(self, instance):
            log before deleting
            instance.destroy()
    """
update_destroy_role = UpdateDestroyRoleView.as_view()