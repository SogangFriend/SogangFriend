from django.urls import re_path, path
from .consumers import *

websocket_urlpatterns = [
    path('ws/Chat/<str:room_name>/<str:member_pk>/', ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]