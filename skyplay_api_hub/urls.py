"""
URL configuration for skyplay_api_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect

# Configure Swagger Schema View
# Define the schema view for Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Encryption/Decryption API",
      default_version='v1',
      description="API for encryption and decryption",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@watcho.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


def redirect_to_admin(request):
    return redirect('/admin')

urlpatterns = [
    path('', lambda request: redirect('/admin/')),  # Redirect root to admin
    path('admin/', admin.site.urls),
    path('settings/', include('setting.urls')),  # Add this line
    path("subscribe/", include("subscribe.urls")),
    path('users/', include('users.urls')),  # Include user URLs
    path("wallet/", include("wallet.urls")),
    path('skyplay_api/', include('skyplay_api.urls')), 

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('api/', include('testapp.urls')),  # Include testapp API
    path('watcho/', include('watcho.urls')),
    path('ott_subscription/', include('ott_subscription.urls')),
]
