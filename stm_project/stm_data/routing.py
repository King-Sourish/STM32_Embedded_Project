from django.urls import path
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sensor-data/$', consumers.SensorDataConsumer.as_asgi()),
    path('ws/sensor-data/', consumers.SensorDataConsumer.as_asgi()),
]
