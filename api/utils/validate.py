from rest_framework import serializers

def clean_data(data):
    if data["username"] == "":
        raise serializers.ValidationError("Username is required")
    if data["password"] == "":
        raise serializers.ValidationError("Password is required")
    
    data["username"] = data["username"].strip().title()
    if data["email"] is not None:
        data["email"] = data["email"].strip().lower()
    
    return data