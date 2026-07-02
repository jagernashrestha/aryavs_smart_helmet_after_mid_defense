"""
api/views/root.py — Public API root view.

GET /api/ returns a simple JSON index of available routes.
This view is intentionally public (AllowAny) to aid demo/testing.
All listed endpoints still enforce their own auth requirements.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    SmartHelmetX API root. Lists available endpoints for reference.
    Endpoint protection is enforced individually — this index is public.
    """
    base = request.build_absolute_uri('/api/')
    return Response({
        'name': 'SmartHelmetX API',
        'version': '1.0',
        'note': 'All endpoints below enforce their own authentication. This index is public.',
        'endpoints': {
            # Auth (public)
            'auth': {
                'register':       base + 'auth/register/',
                'login':          base + 'auth/login/',
                'refresh_token':  base + 'auth/refresh/',
                'profile':        base + 'auth/profile/',        # JWT required
            },
            # Rider endpoints (JWT required)
            'rider': {
                'dashboard':      base + 'dashboard/',
                'alerts':         base + 'alerts/',
                'sensor_history': base + 'sensor-history/',
                'gps_history':    base + 'gps-history/',
                'sos':            base + 'sos/',
                'devices':        base + 'devices/',
                'contacts':       base + 'contacts/',
            },
            # Device endpoints (X-Device-Secret header required)
            'device': {
                'sensor_data':    base + 'sensor-data/',
                'gps':            base + 'gps/',
                'alert':          base + 'alert/',
                'device_config':  base + 'device-config/<device_id>/',
            },
            # Admin endpoints (JWT + staff required)
            'admin': {
                'stats':          base + 'admin/stats/',
                'riders':         base + 'admin/riders/',
                'rider_detail':   base + 'admin/riders/<rider_id>/',
            },
        },
    })
