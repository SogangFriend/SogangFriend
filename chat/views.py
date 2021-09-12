from django.shortcuts import render
from django.views.generic import *

# Create your views here.


class ChatHomeView(View):
    def get(self, request):
        return render(request, 'chat/chat_home.html', {})


class RoomView(View):
    def get(self, request, room_name):
        return render(request, 'chat/room.html',
                      {'room_name': room_name})