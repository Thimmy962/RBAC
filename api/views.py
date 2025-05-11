from rest_framework import status, response, generics
from .utils import serializers
from django.contrib.auth.models import Group
from .permissions import AllModelsPermissionMixin
# Create your views here.


class ListCreateRoleView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Group.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ListGroupSerializer
        return serializers.CreateGroupSerializer
        

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Role Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
list_create_role = ListCreateRoleView.as_view()


class RetrieveUpdateDestroyRoleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.RetrieveUpdateDestroyGroupSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        print(serializer)
        return response.Response("Successful", status = status.HTTP_200_OK)
retrieve_update_destroy_role = RetrieveUpdateDestroyRoleView.as_view()