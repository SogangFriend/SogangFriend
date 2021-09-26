from django.urls import path
from .views import *
app_name = 'Chat'

urlpatterns = [
    path('', ChatHomeView.as_view(), name='index'),
    #path('<str:room_name>/<str:member>/<str:user_nickname>/', RoomView.as_view(), name='room'),
    path('create/', RoomView.as_view(), name='chat_create'),
    #path('chatform/', FormView.as_view(), name='room')
]