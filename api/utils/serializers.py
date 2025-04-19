from rest_framework import serializers
from ..models import User


# User Serializer for creating a user
class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Validate email
    def validate_email(self, value):
        # If email is empty, return it
        if value == "":
            return value
        # If email already exists, raise an error
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already exists")
        return value.lower()
    
    # Validate username
    def validate_username(self, value):
        # username should be unique
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


