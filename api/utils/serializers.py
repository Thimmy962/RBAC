from rest_framework import serializers
from ..models import Staff
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError



# Group Serializer for creating and listing Groups
class CreateGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]

    def validate_name(self, value):
        cleaned = value.strip().title()
        if cleaned == "":
            raise serializers.ValidationError("Group name is required")
        if Group.objects.filter(name=cleaned).exists():
            raise serializers.ValidationError("Group with this name already exists")
        return cleaned
    
    # makes sure that extra fields besides the required is not sent
    def to_internal_value(self, data):
        allowed = set(self.fields)
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions)
        return group
    

    

class ListGroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "members"]

    def get_members(self, obj):
            return [staff.username for staff in obj.user_groups.all()]



# Group Serializer for retrieving, updating and destroying roles/groups
class RetrieveUpdateDestroyGroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "members"]

    def get_members(self, obj):
            return [staff.username for staff in obj.user_groups.all()]
    

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

    # makes sure that extra fields besides the required is not sent
    def to_internal_value(self, data):
        allowed = set(self.fields)
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)


    # This create() method to hash password to solve the double hasing of password
    # if save() method was overwritten in when User model was defined
    def create(self, validated_data):
        password = validated_data.pop("password")
        staff = Staff(**validated_data)
        staff.set_password(password)
        staff.save()
        return staff

    def validate_email(self, value):
        value = value.strip().lower()
        if not value:
            pass
        if Staff.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        value = value.strip().title()
        if not value:
            raise serializers.ValidationError("Username is required")
        if Staff.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_password(self, value):
        try:
            django_validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


#  User serializer for getting, updating and destroying a user
class RetrieveUpdateDestroyStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "username", "email",
          "first_name", "last_name", "phone", 
          "address", "is_staff", "is_active",
            "groups"
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