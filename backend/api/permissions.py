import os
from rest_framework import permissions

# Hardcoded fallback for prototype ease, can be overridden by env variable
EXPECTED_DEVICE_SECRET = os.environ.get('DEVICE_SECRET', 'smarthelmet-proto-secret-123')

class HasDeviceSecret(permissions.BasePermission):
    """
    Allows access only to devices that provide the correct X-DEVICE-SECRET header.
    This is a prototype-level verification to prevent random data injection.
    """
    message = "Invalid or missing X-Device-Secret header."

    def has_permission(self, request, view):
        secret = request.headers.get('X-Device-Secret')
        return secret == EXPECTED_DEVICE_SECRET
