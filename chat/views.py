from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *

from .forms import *
from .models import *
# Create your views here.


class ChatHomeView(View):
    def get(self, request):
        return render(request, 'chat/chat_home.html', {})


class RoomCreateView(View):
    form_class = ChatRoomForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'chat/chat_form.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            Room_Name = form.cleaned_data['Room_Name']
            NickName = form.cleaned_data['NickName']
            member_pk = request.session.get('Member')
            member = Member.objects.get(pk=member_pk)

            chatroom = ChatRoom.objects.create(name=Room_Name, creator=member, created_time=timezone.now(), location=member.location)
            Member_ChatRoom.objects.create(member=member, chat_room=chatroom, member_timestamp=timezone.now(),chat_room_timestamp=timezone.now())


        return render(request, 'homepage.html')

      
class RommView(View):
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
