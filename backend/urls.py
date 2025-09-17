# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({"id": user.id, "name": user.first_name or user.username, "email": user.email})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("properties.urls")),
    path("api/me/", me),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", RedirectView.as_view(url="/api/", permanent=False)),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
