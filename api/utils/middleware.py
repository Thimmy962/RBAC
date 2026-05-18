from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseServerError


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        try:
            user_auth_tuple = self.jwt_auth.authenticate(request)

            if user_auth_tuple is None:
                return JsonResponse(
                    {"detail": "Authentication credentials were not provided."},
                    status=401
                )

            request.user, _ = user_auth_tuple

        except (InvalidToken, AuthenticationFailed):
            return JsonResponse(
                {"detail": "Invalid or expired token."},
                status=401
            )

        return self.get_response(request)

