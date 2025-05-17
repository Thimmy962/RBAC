from rest_framework import status, response, generics
from api.utils import serializers
from django.contrib.auth.models import Group
from api.permissions import AllModelsPermissionMixin
from api.models import Author, Book, Genre
# Create your views here.


# TO CREATE OR LIST BOOK
class ListCreateBookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
list_create_book = ListCreateBookView.as_view()

class RetrieveUpdateDestroyBookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
retrieve_update_destroy_book = RetrieveUpdateDestroyBookView.as_view()


# TO CREATE OR LIST AUTHOR
class ListCreateAuthorView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
list_create_author = ListCreateAuthorView.as_view()


# RETRIEVE, UPDATE OR DESTROY AUTHOR
class RetrieveUpdateDestroyAuthorView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
retrieve_update_destroy_author = RetrieveUpdateDestroyAuthorView.as_view()


# RETRIEVE, UPDATE OR DESTROY AUTHOR
class RetrieveUpdateDestroyAuthorView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
retrieve_update_destroy_author = RetrieveUpdateDestroyAuthorView.as_view()

# TO CREATE OR LIST GENRE
class ListCreateGenreView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
list_create_genre = ListCreateGenreView.as_view()


# RETRIEVE, UPDATE OR DESTROY GENRE
class RetrieveUpdateDestroyGenreView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
retrieve_update_destroy_genre = RetrieveUpdateDestroyGenreView.as_view()


# TO CREATE OR LIST ROLE
class ListCreateRoleView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Group.objects.all().order_by("id")
    serializer_class = serializers.ListCreateRoleSerializer
        

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Role Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
list_create_role = ListCreateRoleView.as_view()


# RETRIEVE, UPDATE OR DESTROY ROLE
class RetrieveUpdateDestroyRoleView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.RetrieveUpdateDestroyRoleSerializer

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return response.Response("Role Deleted Successfully", status = 204)
retrieve_update_destroy_role = RetrieveUpdateDestroyRoleView.as_view()