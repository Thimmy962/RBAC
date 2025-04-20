from rest_framework import serializers
from ..models import User
from django.contrib.auth.models import Group


# Group Serializer for creating and listing Groups
class ListCreateGroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "members"]

    def get_members(self, obj):
            return obj.user_groups.all()



# Group Serializer for retrieving, updating and destroying roles/groups
class RetrieveUpdateDestroyGroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "members"]

    def get_members(self, obj):
            return obj.user_groups.all()

# User Serializer for creating and listing  users
class ListCreateUserSerializer(serializers.ModelSerializer):
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

#  User serializer for getting, updating and destroying a user
class RetrieveUpdateDestroyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email",
          "first_name", "last_name", "phone", 
          "address", "is_staff", "is_active",
            "groups"
        ]

    def validate_email(self, value):
        if value == "":
            return self.instance.email
        value = value.strip().lower()
        if User.objects.filter(email=value).exclude(pk = self.instance.pk).exists():
            raise serializers.ValidationError("Email already exists")
        
        return value
    
    def validate_first_name(self, value):
        if value == "":
            return self.instance.first_name
        value = value.strip().title()
        return value
    
    def validate_last_name(self, value):
        if value == "":
            return self.instance.last_name
        value = value.strip().title()
        return value