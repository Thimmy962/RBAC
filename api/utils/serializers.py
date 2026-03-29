from rest_framework import serializers
from api.models import Staff, Author, Book, Genre
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


# makes sure that extra fields besides the required is not sent
# the csrf token field comes as a security measure with django, so it is been added to the expected fields
# This way it will not be flagged as an unexpected field
class StrictSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        allowed = set(self.fields)
        extra = set(data) - allowed
        if extra:
            raise serializers.ValidationError(
                {key: "Unexpected field" for key in extra}
            )
        return super().to_internal_value(data)

class BookSerializer(StrictSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "genre", "author"]

    def validate_title(self, value):
        clean = value.strip().title()
        if not clean: raise serializers.validationError("Book title required")
        # if Book.objects.filter(title = clean).exclude(pk = self.instance.pk if self.instance else None).exists():
            # return self.instance.title
        if Book.objects.filter(title=clean).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Book with this title already exists")
        return clean


class AuthorSerializer(StrictSerializer):
    books = serializers.SerializerMethodField()
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "books"]

    # books written by this author
    def get_books(self, obj):
        # return [book.title for book in obj.author_books.all()]
        # can also be written as 
        return BookSerializer(obj.author_books.all(), many=True).data
    

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get("view")
        if view and view.__class__.__name__ == "ListCreateAuthorView":
            fields.pop("books", None)
        return fields

    def validate_first_name(self, value):
        cleaned = value.strip().title()
        if not cleaned: raise serializers.validationError("First name is required")
        if Author.objects.filter(first_name = cleaned).exclude(pk = self.instance.pk if self.instance else None):
            return self.instance.first_name
        return cleaned
    
    def validate_last_name(self, value):
        cleaned = value.strip().title()
        if not cleaned: raise serializers.validationError("Last name is required")
        if Author.objects.filter(first_name = cleaned).exclude(pk = self.instance.pk if self.instance else None):
            return self.instance.last_name
        return cleaned


class GenreSerializer(StrictSerializer):
    books = serializers.SerializerMethodField()
    class Meta:
        model = Genre
        fields = ["id", "genre", "books"]

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get("view")
        if view and view.__class__.__name__ == "ListCreateGenreView":
            fields.pop("books", None)
        return fields

    def get_books(self, obj):
        return [book.title for book in obj.genre_books.all()]

    def validate_genre(self, value):
        cleaned = value.strip().title()
        if not cleaned:
            raise serializers.ValidationError("Genre name is required")
        if Genre.objects.filter(genre=cleaned).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Genre with this name already exists")
        return cleaned

    def update(self, instance, validated_data):
        instance.genre = validated_data.get("genre", instance.genre)
        instance.save()
        return instance


# Group Serializer for creating Groups
class ListCreateRoleSerializer(StrictSerializer):
    member_usernames = serializers.SerializerMethodField()

    members = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), many=True, required=False
    )

    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, required=False
    )

    member_count = serializers.SerializerMethodField()
    permission_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id", "name",
            "members", "member_usernames",
            "permissions",
            "member_count", "permission_count"
        ]

    def get_member_usernames(self, obj):
        return [staff.username for staff in obj.user_groups.all()]

    def get_member_count(self, obj):
        return obj.user_groups.count()

    def get_permission_count(self, obj):
        return obj.permissions.count()

    def validate_name(self, value):
        cleaned = value.strip().title()
        if not cleaned:
            raise serializers.ValidationError("Group name is required")
        if Group.objects.filter(name=cleaned).exists():
            raise serializers.ValidationError("Group with this name already exists")
        return cleaned

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        members = validated_data.pop("members", [])

        group = Group.objects.create(**validated_data)

        if permissions:
            group.permissions.set(permissions)

        if members:
            group.user_groups.set(members)

        return group


# Group Serializer for retrieving, updating and destroying roles/groups
class RetrieveUpdateDestroyRoleSerializer(StrictSerializer):
    member_usernames = serializers.SerializerMethodField()
    permission_codenames = serializers.SerializerMethodField()

    members = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), many=True, required=False
    )

    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, required=False
    )

    member_count = serializers.SerializerMethodField()
    permission_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id", "name",
            "members", "member_usernames",
            "permissions", "permission_codenames",
            "member_count", "permission_count"
        ]

    def get_member_usernames(self, obj):
        return [staff.username for staff in obj.user_groups.all()]

    def get_member_count(self, obj):
        return obj.user_groups.count()

    def get_permission_count(self, obj):
        return obj.permissions.count()

    def get_permission_codenames(self, obj):
        return [perm.codename for perm in obj.permissions.all()]

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions", None)
        members = validated_data.pop("members", None)

        instance.name = validated_data.get("name", instance.name)
        instance.save()

        if permissions is not None:
            instance.permissions.set(permissions)

        if members is not None:
            instance.user_groups.set(members)

        return instance

    
class ListStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['username', 'email', "first_name", "last_name"]


# User Serializer for creating  users
class CreateStaffSerializer(StrictSerializer):
    class Meta:
        model = Staff
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # this hides the password in API responses
        }

    # This create() method to hash password to solve the double hasing of password
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