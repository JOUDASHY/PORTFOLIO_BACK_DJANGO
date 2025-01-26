# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns  # Importez vos URL WebSocket depuis routing.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_django_portfolio_me.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Utilisez vos URL WebSocket ici
        )
    ),
})
