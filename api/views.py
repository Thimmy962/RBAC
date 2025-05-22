from rest_framework import status, response, generics, decorators
from api.utils import serializers
from django.contrib.auth.models import Group
from api.permissions import AllModelsPermissionMixin
from api.models import Author, Book, Genre
# Create your views here.


# TO CREATE BOOK
class CreateBookView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
create_book = CreateBookView.as_view()

# UPDATE OR DESTROY Book
class UpdateDestroyBookView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
update_destroy_book = UpdateDestroyBookView.as_view()


# TO CREATE AUTHOR
class CreateAuthorView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
create_author = CreateAuthorView.as_view()


# UPDATE OR DESTROY AUTHOR
class UpdateDestroyAuthorView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
update_destroy_author = UpdateDestroyAuthorView.as_view()


# TO CREATE GENRE
class CreateGenreView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
create_genre = CreateGenreView.as_view()


# RETRIEVE, UPDATE OR DESTROY GENRE
class UpdateDestroyGenreView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
update_destroy_genre = UpdateDestroyGenreView.as_view()


# TO CREATE OR LIST ROLE
class CreateRoleView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Group.objects.all().order_by("id")
    serializer_class = serializers.CreateRoleSerializer
        

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Role Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
create_role = CreateRoleView.as_view()


# RETRIEVE, UPDATE OR DESTROY ROLE
class UpdateDestroyRoleView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.UpdateDestroyRoleSerializer

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return response.Response("Role Deleted Successfully", status = 204)
update_destroy_role = UpdateDestroyRoleView.as_view()