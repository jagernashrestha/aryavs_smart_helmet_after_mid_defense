"""
SmartHelmetX project URL configuration.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),
    # Redirect root to /api/
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    # All API endpoints defined in the api app
    path('api/', include('api.urls')),
]
