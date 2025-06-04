# All the serializers here are for deleting and updating models alone
# All the serializers here for for creating models alone

from rest_framework import serializers
from api.models import Staff, Author, Book, Genre
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


class UpdateDeleteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "genre", "author"]


    def validate_title(self, value):
        clean = value.strip().title()
        if not clean:
            id = self.instance.id
            return Book.objects.get(pk = id).title
        if Book.objects.filter(title=clean).exists():
            raise serializers.ValidationError(f"Book with this title: '{clean}' already exists")
        return clean
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    
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


class UpdateDeleteAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name"]
    
    #This is for updating
    def validate_first_name(self, value):
        cleaned = value.strip().title()
        if not cleaned: # If no first name is given while updating this author use the first name previously on the DB
            id =self.instance.id
            return Author.object.get(pk = id).first_name
        return cleaned
    
    def validate_last_name(self, value):
        cleaned = value.strip().title()
        if not cleaned: # If no last name is given while updating this author use the last name previously on the DB
            id =self.instance.id
            return Author.object.get(pk = id).last_name
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


class UpdateDeleteGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "genre"]


    def validate_genre(self, value):
        cleaned = value.strip().title()
        if not cleaned:
            id = self.instance.id
            return Genre.objects.get(pk = id).genre
        if Genre.object.get(genre = cleaned).exists():
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



# Group Serializer for updating and destroying roles/groups
class UpdateDestroyRoleSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ["id", "name", "members", "permissions"]

    def get_members(self, obj):
            return [staff.username for staff in obj.user_groups.all()]
    

    def validate_name(self, value):
        cleaned = value.strip().title()
        if not cleaned:
            raise serializers.ValidationError("Group name is required")
        
        if Group.objects.get(name = cleaned).exists():
            raise serializers.ValidationError("Group with this name already Exists")
        
        return cleaned


#  User serializer for getting, updating and destroying a user
class UpdateDestroyStaffSerializer(serializers.ModelSerializer):
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