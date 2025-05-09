from rest_framework import generics, response, status
from ..permissions import AllModelsPermissionMixin
from ..models import Staff
from . import serializers, validate





class ListCreateViewStaffView(AllModelsPermissionMixin, generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateStaffSerializer
        return serializers.ListStaffSerializer


    def post(self, request, *args, **kwargs):
        copied_data = request.data.copy() # request.data is immutable, hence we need to copy it before cleaning it

        cleaned_data = validate.clean_data(copied_data)
        serializer = self.get_serializer(data=cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
list_create_staff = ListCreateViewStaffView.as_view()


class RetrieveUpdateDestroyStaffView(AllModelsPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = serializers.RetrieveUpdateDestroyStaffSerializer
retrieve_update_destroy_staff = RetrieveUpdateDestroyStaffView.as_view()
