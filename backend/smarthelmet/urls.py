"""
SmartHelmetX project URL configuration.
"""
from django.urls import path, include

urlpatterns = [
    # All API endpoints defined in the api app
    path('api/', include('api.urls')),
]
