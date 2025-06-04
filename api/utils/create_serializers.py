# All the serializers here for for creating models alone

from rest_framework import serializers
from api.models import Staff, Author, Book, Genre
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "genre", "author"]


    def validate_title(self, value):
        clean = value.strip().title()
        if not clean:
            raise serializers.ValidationError("Book title required")
        if Book.objects.filter(title=clean).exists():
            raise serializers.ValidationError(f"Book with this title: '{clean}' already exists")
        return clean

    
        # makes sure that extra fields besides the required is not sent
    def to_internal_value(self, data):
        allowed = set(self.fields)
        # django middleware adds csrfmiddlewaretoken field with a token for safety which is not part of the allowed serialized fields defined above
        # The line below adds csrfmiddlewaretoken field to the allowed fields   
        allowed.add('csrfmiddlewaretoken')
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)


class CreateAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name"]
    

    def validate_first_name(self, value):
        cleaned = value.strip().title()
        if not cleaned: # If no first name is given while creating this author raise an error
            raise serializers.validationError("First name is required")
        return cleaned
    
    def validate_last_name(self, value):
        cleaned = value.strip().title()
        if not cleaned:
            raise serializers.validationError("Last name is required")
        return cleaned
    
        # makes sure that extra fields besides the required is not sent
    def to_internal_value(self, data):
        allowed = set(self.fields)
        allowed.add('csrfmiddlewaretoken')
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)


class CreateGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "genre"]


    def validate_genre(self, value):
        cleaned = value.strip().title()
        if not cleaned:
            raise serializers.ValidationError("Genre name is required")
        if Genre.objects.get(genre = cleaned).exists():
            raise serializers.ValidationError("Genre with this name already Exists")
        return cleaned


        # makes sure that extra fields besides the required is not sent
    def to_internal_value(self, data):
        allowed = set(self.fields)
        allowed.add('csrfmiddlewaretoken')
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)


# Group Serializer for creating Groups
class CreateRoleSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset = Staff.objects.all(), many = True, write_only =True
    )

    class Meta:
        model = Group
        fields = ["id", "name", "members", "permissions"]

    def validate_name(self, value):
        cleaned = value.strip().title()
        if not cleaned:
            raise serializers.ValidationError("Group name is required")
        
        if Group.objects.get(name = cleaned).exists():
            raise serializers.ValidationError("Group with this name already Exists")
        
        return cleaned
    
    # makes sure that extra fields besides the required is not sent
    def to_internal_value(self, data):
        allowed = set(self.fields)
        allowed.add('csrfmiddlewaretoken')
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)


    def create(self, validated_data):
        members = validated_data.pop("members", [])
        permissions = validated_data.pop("permissions", [])
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions)
        for member in members:
                member.groups.add(group)
        return group


# User Serializer for creating  users
class CreateStaffSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        queryset = Group.objects.all(), many = True, write_only =True
    )
    class Meta:
        model = Staff
        fields = ['username', 'email', 'password', 'roles']
        extra_kwargs = {
            'password': {'write_only': True}  # this hides the password in API responses
        }

    # makes sure that extra fields besides the required are not sent
    def to_internal_value(self, data):
        allowed = set(self.fields)
        allowed.add('csrfmiddlewaretoken')
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)

    # This create() method to hash password to solve the double hasing of password
    def create(self, validated_data):
        password = validated_data.pop("password")
        roles = validated_data.pop("roles", [])
        staff = Staff(**validated_data)
        staff.set_password(password)
        staff.save()
        staff.groups.set(roles)
        return staff

    def validate_email(self, value):
        value = value.strip().lower()
        if not value:
            pass
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
