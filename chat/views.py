from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import *
from .models import *

# Create your views here.


class ChatHomeView(View):
    def get(self, request):
        return render(request, 'chat/chat_home.html', {})


class RoomView(View):
    def get(self, request, room_name):
        if ChatRoom.objects.filter(pk=room_name).count() == 0:
            return HttpResponse('방이 없습니다')
        member_pk = request.session.get('Member')
        return render(request, 'chat/room.html',
                      {'room_name': room_name, 'member_pk': member_pk})


class ChatListView(View):
    def get(self, request):
        rooms = ChatRoom.objects.all()
        return render(request, 'chat/room_list.html',
                      {'rooms': rooms})