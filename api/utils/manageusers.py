from rest_framework import generics, response, status
from api.permissions import AllModelsPermissionMixin
from api.models import Staff
from api.utils import serializers





class CreateViewStaffView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = serializers.CreateStaffSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response("Created Successfully", status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
create_staff = CreateViewStaffView.as_view()


class UpdateDestroyStaffView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = serializers.UpdateDestroyStaffSerializer
update_destroy_staff = UpdateDestroyStaffView.as_view()
