"""this file will contain evertyting that related to WS."""

from django.urls import re_path, path

from cshr.consumers.notifications_consumer import NotificationConsumer

websocket_urlpatterns = [
    # re_path(r'ws/notification/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
    path("ws/notification/<str:room_id>/", NotificationConsumer.as_asgi()),
]
