from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Property, Favorite
from .serializers import PropertySerializer, FavoriteSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class PropertyListView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        qs = Property.objects.all()
        location = self.request.query_params.get('location')
        return qs.filter(location__icontains=location) if location else qs
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

class FavoriteToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            prop = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fav, created = Favorite.objects.get_or_create(user=request.user, property=prop)
        if not created:
            fav.delete()
            return Response({"status": "unfavorited"})
        return Response({"status": "favorited"})

class UserFavoritesView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Property.objects.filter(favorite__user=self.request.user)
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx
