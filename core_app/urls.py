
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users_app.views import UserListView, UserDetailsView

# from django.contrib import admin
from django.urls import path, re_path

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API documentation for your Django project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users', UserListView.as_view(), name='users'),
    path('users/<uuid:id>/', UserDetailsView.as_view(), name='user-detail'),
]
