from django.urls import path
from .views import *
app_name = 'Chat'

urlpatterns = [
    path('', ChatListView.as_view(), name='list'),
    path('new/', RoomCreateView.as_view(), name='chat_create'),
    path('list/', ChatListView.as_view(), name='list'),
    path('<str:room_name>/', RoomView.as_view(), name='room'),
    path('dm/<str:pk>/', EnterDMView.as_view(), name='dm'),
]
