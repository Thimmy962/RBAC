from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.http import HttpResponseServerError

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


# Maintenance mode middleware
class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        if settings.MAINTENANCE_MODE:
            return HttpResponseServerError("Site Under maintenance")
        return self.get_response(request)
            
