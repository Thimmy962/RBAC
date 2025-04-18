from django.shortcuts import render
from rest_framework import status, response
from rest_framework import decorators
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.


@decorators.api_view(['GET'])
@decorators.permission_classes([])
def index(request):

    return response.Response("Hello", status = status.HTTP_200_OK)


@decorators.api_view(['POST'])
def create_grp(request):
    pass




@decorators.api_view(['PATCH'])
def edit_grp(request):
    pass



@decorators.api_view(['DELETE'])
def delete_grp(request):
    pass
