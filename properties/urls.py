# properties/urls.py
from django.urls import path
from django.http import JsonResponse
from .views import (
    PropertyListView, PropertyDetailView, UserRegistrationView,
    UserLoginView, FavoriteToggleView, UserFavoritesView
)

def api_root(request):
    # return a simple index for /api/
    return JsonResponse({
        "register": "/api/register/",
        "login": "/api/login/",
        "properties": "/api/properties/",
        "favorites": "/api/favorites/",
    })

urlpatterns = [
    path("", api_root, name="api-root"),  # handles /api/
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("properties/", PropertyListView.as_view(), name="property-list"),
    path("properties/<int:pk>/", PropertyDetailView.as_view(), name="property-detail"),
    path("properties/<int:pk>/favorite/", FavoriteToggleView.as_view(), name="favorite-toggle"),
    path("favorites/", UserFavoritesView.as_view(), name="user-favorites"),
]
