from rest_framework import generics, response, status
from api.permissions import AllModelsPermissionMixin
from api.models import Staff
from api.utils import serializers





class ListCreateViewStaffView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = serializers.CreateStaffSerializer
        
create_staff = ListCreateViewStaffView.as_view()


class UpdateDestroyStaffView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = serializers.UpdateDestroyStaffSerializer
update_destroy_staff = UpdateDestroyStaffView.as_view()
