"""
api/views/sos.py — Manual SOS triggered from the web dashboard.

This endpoint is for the FRONTEND only (JWT required).
The ESP32 firmware posts crash/fall alerts to /api/alert/ instead,
which accepts device_id and does not require a user JWT.

Flow:
  1. User presses SOS on the web dashboard.
  2. Backend creates a critical SOS alert and broadcasts it over WebSocket.
  3. Emergency contacts are returned so the dashboard can display them.
     NOTE: The backend does NOT send SMS — SMS is handled by the ESP32 firmware
           via the SIM800L GSM module. The contacts list here is for display only.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import EmergencyContact, HelmetDevice, GPSLocation
from ..serializers import AlertSerializer, EmergencyContactSerializer
from ..services import create_alert


class SOSTriggerView(APIView):
    """Manual SOS from the web dashboard (JWT-authenticated riders only)."""

    def post(self, request):
        device = HelmetDevice.objects.filter(user=request.user).first()
        if not device:
            return Response(
                {'error': 'No device registered for this account.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Use the most recent GPS fix so the alert has a location if available
        latest_gps = GPSLocation.objects.filter(device=device).first()

        alert = create_alert(
            device=device,
            alert_type='sos',
            severity='critical',
            message='Manual SOS triggered from web dashboard.',
            latitude=latest_gps.latitude if latest_gps else None,
            longitude=latest_gps.longitude if latest_gps else None,
        )

        # Return contacts so the dashboard can DISPLAY them.
        # This backend does NOT send SMS — that is handled by the ESP32 firmware.
        contacts = EmergencyContact.objects.filter(user=request.user)

        return Response({
            'alert': AlertSerializer(alert).data,
            # Renamed from contacts_notified → contacts (accurate: display only)
            'contacts': EmergencyContactSerializer(contacts, many=True).data,
            'message': 'SOS alert created. SMS is sent by the helmet device firmware.',
        }, status=status.HTTP_201_CREATED)
