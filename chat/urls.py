from django.urls import path
from .views import *
app_name = 'Chat'

urlpatterns = [
    path('', ChatHomeView.as_view(), name='index'),
    path('create/', RoomCreateView.as_view(), name='Chat_create'),
    path('list/', ChatListView.as_view(), name='list'),
    path('enter/<str:room_name>/', RoomView.as_view(), name='room'),
    path('enter/dm/<str:pk>/', EnterDMView.as_view(), name='dm'),
]
