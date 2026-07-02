from .auth import RegisterView, ProfileView
from .device import DeviceViewSet, SensorDataView, GPSDataView, DeviceConfigView
from .alerts import AlertCreateView, AlertListView, AlertActionView
from .dashboard import DashboardView, SensorHistoryView, GPSHistoryView
from .sos import SOSTriggerView
from .admin_views import AdminStatsView, AdminRiderListView, AdminRiderDetailView

__all__ = [
    'RegisterView', 'ProfileView',
    'DeviceViewSet', 'SensorDataView', 'GPSDataView', 'DeviceConfigView',
    'AlertCreateView', 'AlertListView', 'AlertActionView',
    'DashboardView', 'SensorHistoryView', 'GPSHistoryView',
    'SOSTriggerView',
    'AdminStatsView', 'AdminRiderListView', 'AdminRiderDetailView',
]

