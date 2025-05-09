from rest_framework import serializers
from ..models import Staff
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
    

class ListStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['username', 'email', "first_name", "last_name"]


# User Serializer for creating  users
class CreateStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # this hides the password in API responses
        }

    # This create() method to hash password to solve the double hasing of password
    # if save() method was overwritten in when User model was defined
    def create(self, validated_data):
        password = validated_data.pop("password")
        staff = Staff(**validated_data)
        staff.set_password(password)
        staff.save()
        return staff

    def validate_email(self, value):
        if value == "":
            return value
        if Staff.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already exists")
        return value.lower()

    def validate_username(self, value):
        if Staff.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

#  User serializer for getting, updating and destroying a user
class RetrieveUpdateDestroyStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["username", "email",
          "first_name", "last_name", "phone", 
          "address", "is_staff", "is_active",
            "groups", "password"
        ]

    def validate_email(self, value):
        if value == "":
            return self.instance.email
        value = value.strip().lower()
        if Staff.objects.filter(email=value).exclude(pk = self.instance.pk).exists():
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