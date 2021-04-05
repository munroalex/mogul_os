"""
ASGI config for mogul_os project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mogul_os.settings')
django.setup()
from asgiref.compatibility import guarantee_single_callable,double_to_single_callable

from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import mogul_backend.routing
from mogul_backend.consumers import DiscordConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mogul_backend.routing.websocket_urlpatterns
        )
    ),
    'discord': DiscordConsumer,
    # Just HTTP for now. (We can add other protocols later.)
})