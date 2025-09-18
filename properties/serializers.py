# properties/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Property, Favorite

PLACEHOLDER = "https://picsum.photos/600/400"
GALLERY = [
    "https://picsum.photos/id/274/800/500",
    "https://picsum.photos/id/204/800/500",
    "https://picsum.photos/id/248/800/500",
    "https://picsum.photos/id/241/800/500",
    "https://picsum.photos/id/218/800/500",
]

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(User.objects.all(), message="Username already taken")]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PropertySerializer(serializers.ModelSerializer):
    # New computed fields for images and demo meta the UI already references
    image_url = serializers.SerializerMethodField()
    detail_images = serializers.SerializerMethodField()
    days_ago = serializers.SerializerMethodField()
    avg_price = serializers.SerializerMethodField()
    is_villa = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    seller_contact = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            "id", "title", "description", "price", "location",
            "image", "bedrooms", "bathrooms",
            "image_url", "detail_images",
            "days_ago", "avg_price", "is_villa",
            "seller_name", "seller_contact",
        )

    def _abs(self, url):
        request = self.context.get("request")
        if request and url and not str(url).startswith("http"):
            return request.build_absolute_uri(url)
        return url

    def get_image_url(self, obj):
        if getattr(obj, "image", None) and hasattr(obj.image, "url"):
            return self._abs(obj.image.url)
        return PLACEHOLDER

    def get_detail_images(self, obj):
        imgs = []
        if getattr(obj, "image", None) and hasattr(obj.image, "url"):
            imgs.append(self._abs(obj.image.url))
        # Add 4 stock gallery images to enrich the page
        imgs.extend(GALLERY[:4])
        return imgs

    # Light demo helpers to satisfy current UI fields; replace later with real data
    def get_days_ago(self, obj):
        return 7  # constant placeholder; wire to a timestamp when available

    def get_avg_price(self, obj):
        try:
            return int(obj.price)  # simple echo as placeholder
        except Exception:
            return 0

    def get_is_villa(self, obj):
        try:
            return int(obj.bedrooms or 0) >= 3
        except Exception:
            return False

    def get_seller_name(self, obj):
        return "Urbo Ventures"

    def get_seller_contact(self, obj):
        return "0000000000"

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "user", "property")
