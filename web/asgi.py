import os
import django
from django.core.asgi import get_asgi_application

# اول Django رو setup کن
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

# سپس بقیه import ها
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.waiter.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.waiter.routing.websocket_urlpatterns
        )
    ),
})