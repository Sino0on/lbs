from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = [
    path('ws/socket-server/chat/<str:pk>', ChatConsumers.as_asgi()),
]