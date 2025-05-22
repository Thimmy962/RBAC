from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class SimpleJWTGraphQLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        try:
            user_auth_tuple = self.jwt_auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, _ = user_auth_tuple
            else:
                request.user = AnonymousUser()
        except Exception:
            request.user = AnonymousUser()
        return self.get_response(request)
