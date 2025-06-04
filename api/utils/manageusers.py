from rest_framework import generics
from api.permissions import AllModelsPermissionMixin
from api.models import Staff
from api.utils import create_serializers, update_delete_serializers





class ListCreateViewStaffView(AllModelsPermissionMixin, generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = create_serializers.CreateStaffSerializer
        
create_staff = ListCreateViewStaffView.as_view()


class UpdateDestroyStaffView(AllModelsPermissionMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = update_delete_serializers.UpdateDestroyStaffSerializer
update_destroy_staff = UpdateDestroyStaffView.as_view()
