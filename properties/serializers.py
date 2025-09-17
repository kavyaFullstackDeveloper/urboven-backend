# properties/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Property, Favorite

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(User.objects.all(), message="Username already taken")]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")
        extra_kwargs = {"email": {"required": False, "allow_blank": True},
                        "first_name": {"required": False, "allow_blank": True},
                        "last_name": {"required": False, "allow_blank": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "user", "property")
