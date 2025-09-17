from django.urls import path
from .views import (
    PropertyListView,
    PropertyDetailView,
    UserRegistrationView,
    UserLoginView,
    FavoriteToggleView,
    UserFavoritesView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('properties/<int:pk>/favorite/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', UserFavoritesView.as_view(), name='user-favorites'),
]