from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenViewBase, Request, Response, status
)
from django.contrib import admin
from django.urls import path, include

def clean_data(data):
    if data["username"] is not None:
        data["username"] = data["username"].title()
    return data

"""
    Default simple jwt is case sensitive with username
    Since registering a user runs the title function on the username before saving to database
    The same should be done on the username while trying to log a user in so username becomes case insensitive
    Hence the CustomViewBase written by me:
        Inherits from the TokenObtainPairView of Simple_JWT
        Overides the default post function to clean data and before trying to log user in
"""
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = clean_data(request.data.copy())
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include("api.urls")),
]
