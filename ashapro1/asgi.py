"""
ASGI config for ashapro1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path
from ashaapp1.consumers import ChatConsumer
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ashapro1.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'^ws/chat/(?P<user_id>\d+)/$', ChatConsumer.as_asgi()),
            ])
        )
    ),
})
