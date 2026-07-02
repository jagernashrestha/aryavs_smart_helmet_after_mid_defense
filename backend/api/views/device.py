from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permissions import HasDeviceSecret

from ..models import EmergencyContact, HelmetDevice, SensorReading, GPSLocation
from ..serializers import (
    EmergencyContactSerializer, HelmetDeviceSerializer,
    SensorDataInputSerializer, GPSInputSerializer,
)
from ..services import (
    get_device_or_404,
    mark_device_online,
    broadcast_sensor_update,
    broadcast_gps_update,
)


# ============ EMERGENCY CONTACTS ============

class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============ DEVICE ============

class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = HelmetDeviceSerializer

    def get_queryset(self):
        return HelmetDevice.objects.filter(user=self.request.user)


# ============ SENSOR DATA (ESP32 Endpoint) ============

class SensorDataView(APIView):
    """Receive accelerometer/gyroscope readings from the ESP32."""
    permission_classes = [HasDeviceSecret]  # Prototype device verification

    def post(self, request):
        serializer = SensorDataInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        device = get_device_or_404(data['device_id'])
        if device is None:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        # Every valid sensor packet = device is alive
        mark_device_online(device)

        reading = SensorReading.objects.create(
            device=device,
            acc_x=data['acc_x'],
            acc_y=data['acc_y'],
            acc_z=data['acc_z'],
            gyro_x=data.get('gyro_x', 0),
            gyro_y=data.get('gyro_y', 0),
            gyro_z=data.get('gyro_z', 0),
        )

        broadcast_sensor_update(reading)

        return Response({'status': 'ok', 'id': reading.id}, status=status.HTTP_201_CREATED)


# ============ GPS DATA (ESP32 Endpoint) ============

class GPSDataView(APIView):
    """Receive GPS location from the ESP32."""
    permission_classes = [HasDeviceSecret]

    def post(self, request):
        serializer = GPSInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        device = get_device_or_404(data['device_id'])
        if device is None:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        # Every valid GPS packet = device is alive (was missing before)
        mark_device_online(device)

        location = GPSLocation.objects.create(
            device=device,
            latitude=data['latitude'],
            longitude=data['longitude'],
            speed=data.get('speed', 0),
            altitude=data.get('altitude', 0),
            accuracy=data.get('accuracy', 0),
        )

        broadcast_gps_update(location)

        return Response({'status': 'ok', 'id': location.id}, status=status.HTTP_201_CREATED)


# ============ DEVICE CONFIG (ESP32 Endpoint) ============

class DeviceConfigView(APIView):
    """Serve device configurations (e.g. thresholds) to the ESP32."""
    permission_classes = [HasDeviceSecret]

    def get(self, request, device_id):
        device = get_device_or_404(device_id)
        if device is None:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'device_id': device.device_id,
            'name': device.name,
            'fall_threshold': device.fall_threshold,
            'no_move_timeout': device.no_move_timeout,
            'firmware_version': device.firmware_version,
        }, status=status.HTTP_200_OK)
