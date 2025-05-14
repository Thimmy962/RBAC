from rest_framework import status, response, generics
from api.utils import serializers
from django.contrib.auth.models import Group
from api.permissions import AllModelsPermissionMixin
from api.models import Author, Book, Genre
# Create your views here.

class ListCreateGenreView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
list_create_genre = ListCreateGenreView.as_view()


class RetrieveUpdateDestroygenreView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
retrieve_update_destroy_genre = RetrieveUpdateDestroygenreView.as_view()


class ListCreateRoleView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Group.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ListRoleSerializer
        return serializers.CreateRoleSerializer
        

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Role Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
list_create_role = ListCreateRoleView.as_view()


class RetrieveRoleView(AllModelsPermissionMixin, generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.RetrieveRoleSerializer
retrieve_role = RetrieveRoleView.as_view()