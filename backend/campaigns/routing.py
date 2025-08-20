from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/campaigns/(?P<campaign_id>\w+)/$', consumers.CampaignConsumer.as_asgi()),
    re_path(r'ws/dashboard/$', consumers.DashboardConsumer.as_asgi()),
    re_path(r'ws/admin/monitoring/$', consumers.AdminMonitoringConsumer.as_asgi()),
]
