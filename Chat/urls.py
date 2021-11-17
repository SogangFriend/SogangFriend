from django.urls import path
from .views import *
app_name = 'Chat'

urlpatterns = [
    path('', ChatView.as_view(), name='room'),
    path('new/', RoomCreateView.as_view(), name='chat_create'),
    path('list/', ChatListView.as_view(), name='list'),
    path('dm/<str:pk>/', EnterDMView.as_view(), name='dm'),
]
