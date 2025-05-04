import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from django_eventstream import eventstream

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "eventstream": eventstream,
})
