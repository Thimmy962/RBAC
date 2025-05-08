from rest_framework import generics, response, status
from ..permissions import AllModelsPermissionMixin
from ..models import User
from . import serializers, validate





class ListCreateViewUserView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = User.objects.all()
    

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateUserSerializer
        return serializers.ListUserSerializer


    def post(self, request, *args, **kwargs):
        copied_data = request.data.copy() # request.data is immutable, hence we need to copy it before cleaning it

        cleaned_data = validate.clean_data(copied_data)
        serializer = self.get_serializer(data=cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
list_Create_user = ListCreateViewUserView.as_view()


class RetrieveUpdateDestroyUserView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
retrieve_update_destroy_user = RetrieveUpdateDestroyUserView.as_view()
