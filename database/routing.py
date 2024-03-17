from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path("update/", consumers.SolServerConsumer.as_asgi()),
    re_path("client/", consumers.ClientConsumer.as_asgi(), name='client'),
]