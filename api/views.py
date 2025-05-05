from rest_framework import status, response, generics
from .utils import serializers
from django.contrib.auth.models import Group
from .permissions import ManageUserPermissionMixin
# Create your views here.


class ListCreateRoleView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.ListCreateGroupSerializer

    # def post(self, request, *args, **kwargs):
    #     print(request.data)
    #     return response.Response("Successful", status = status.HTTP_200_OK)
list_create_role = ListCreateRoleView.as_view()


class RetrieveUpdateDestroyRoleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.RetrieveUpdateDestroyGroupSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        print(serializer)
        return response.Response("Successful", status = status.HTTP_200_OK)
retrieve_update_destroy_role = RetrieveUpdateDestroyRoleView.as_view()