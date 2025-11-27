# apps/waiter/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/waiter/orders/(?P<restaurant_id>\w+)/$', consumers.OrderConsumer.as_asgi()),
    re_path(r'ws/waiter/notifications/(?P<waiter_id>\w+)/$', consumers.WaiterNotificationConsumer.as_asgi()),
]