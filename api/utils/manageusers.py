from rest_framework import generics, response, status
from api.permissions import AllModelsPermissionMixin
from api.models import Staff
from api.utils import serializers





class ListCreateViewStaffView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateStaffSerializer
        return serializers.ListStaffSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
list_create_staff = ListCreateViewStaffView.as_view()


class RetrieveUpdateDestroyStaffView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = serializers.RetrieveUpdateDestroyStaffSerializer
retrieve_update_destroy_staff = RetrieveUpdateDestroyStaffView.as_view()
