from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/<str:member_pk>/', ChatConsumer.as_asgi()),
    # re_path(r'ws/Chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]