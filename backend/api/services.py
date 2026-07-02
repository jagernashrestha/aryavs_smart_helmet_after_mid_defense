"""
api/services.py — Shared helpers for device management and WebSocket broadcasts.

These helpers exist to eliminate repeated boilerplate across SensorDataView,
GPSDataView, and AlertCreateView, and to make the device heartbeat behaviour
consistent and easy to understand.
"""

from django.utils import timezone

from .models import HelmetDevice
from .utils import broadcast_to_dashboard

# How many seconds of silence before we consider a device offline.
OFFLINE_THRESHOLD_SECONDS = 60


# ── Device lookup ──────────────────────────────────────────────────────────────

def get_device_or_404(device_id):
    """
    Return the HelmetDevice with the given device_id, or None if not found.

    Usage in views:
        device = get_device_or_404(device_id)
        if device is None:
            return Response({'error': 'Device not found'}, status=404)
    """
    try:
        return HelmetDevice.objects.get(device_id=device_id)
    except HelmetDevice.DoesNotExist:
        return None


# ── Device heartbeat ───────────────────────────────────────────────────────────

def mark_device_online(device):
    """
    Mark a device as online and refresh its last_seen timestamp.

    Called every time valid sensor or GPS data is received from a device.
    Uses update_fields so we only touch the two columns that change.
    """
    device.status = 'online'
    device.save(update_fields=['status', 'last_seen'])


def is_device_online(device):
    """
    Return True if the device reported in within OFFLINE_THRESHOLD_SECONDS.

    This is a simple time-based check — no background workers needed.
    You can call this from the dashboard view or admin to show live status.
    """
    if not device.last_seen:
        return False
    age = (timezone.now() - device.last_seen).total_seconds()
    return age <= OFFLINE_THRESHOLD_SECONDS


# ── WebSocket broadcasts ───────────────────────────────────────────────────────

def broadcast_sensor_update(reading):
    """Push a sensor reading to all connected dashboard WebSocket clients."""
    broadcast_to_dashboard('sensor', {
        'acc_x':     reading.acc_x,
        'acc_y':     reading.acc_y,
        'acc_z':     reading.acc_z,
        'gyro_x':    reading.gyro_x,
        'gyro_y':    reading.gyro_y,
        'gyro_z':    reading.gyro_z,
        'timestamp': reading.timestamp.isoformat(),
    })


def broadcast_gps_update(location):
    """Push a GPS location to all connected dashboard WebSocket clients."""
    broadcast_to_dashboard('gps', {
        'latitude':  location.latitude,
        'longitude': location.longitude,
        'speed':     location.speed,
        'timestamp': location.timestamp.isoformat(),
    })


def broadcast_alert_update(alert):
    """Push a new alert to all connected dashboard WebSocket clients."""
    broadcast_to_dashboard('alert', {
        'id':         alert.id,
        'alert_type': alert.alert_type,
        'severity':   alert.severity,
        'latitude':   alert.latitude,
        'longitude':  alert.longitude,
        'message':    alert.message,
        'created_at': alert.created_at.isoformat(),
    })


# ── Alert creation ─────────────────────────────────────────────────────────────

def create_alert(device, alert_type, severity='high', message='',
                 latitude=None, longitude=None, acc_magnitude=0):
    """
    Create an Alert, broadcast it over WebSocket, and return it.

    Shared by SOSTriggerView (manual web SOS) and AlertCreateView (ESP32).
    Keeps the create+broadcast pair in one place so it's impossible to
    broadcast without saving, or save without broadcasting.
    """
    from .models import Alert   # local import avoids circular dependency

    alert = Alert.objects.create(
        device=device,
        alert_type=alert_type,
        severity=severity,
        message=message,
        latitude=latitude,
        longitude=longitude,
        acc_magnitude=acc_magnitude,
    )
    broadcast_alert_update(alert)
    return alert
