# #
# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LogisticBrockerSystem.settings')
#
# application = get_asgi_application()

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
django_asgi_app = get_asgi_application()
from channels.auth import AuthMiddlewareStack
import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LogisticBrockerSystem.settings')


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})