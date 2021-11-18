from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import *

from .forms import *
from .models import *
# Create your views here.


class RoomCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/create/'
    form_class = ChatRoomForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'Chat/chat_form.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            nick_name = form.cleaned_data['nick_name']
            member_pk = request.session.get('member')
            member = Member.objects.get(pk=member_pk)

            chatroom = ChatRoom.objects.create(name=room_name, creator=member,
                                               created_time=timezone.now(), location=member.location)
            Member_ChatRoom.objects.create(member=member, chat_room=chatroom, member_timestamp=timezone.now())

        return redirect('/Chat/list')

      
class ChatView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/'

    def get(self, request):
        member_pk = request.session.get('member')
        member = Member.objects.get(pk=member_pk)
        rooms = Member_ChatRoom.objects.filter(member=member)
        return render(request, 'Chat/chat_test.html',
                      {'rooms': rooms, 'member_pk': member_pk})


class ChatListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/list/'

    def get(self, request):
        rooms = ChatRoom.objects.all()
        return render(request, 'Chat/room_list.html',
                      {'rooms': rooms})


class EnterDMView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/list/'

    def get(self, request, pk):
        target = Member.objects.get(pk=pk)
        me = Member.objects.get(pk=request.session.get('member'))
        mc = me.chats.filter(target=target, is_dm=True)
        if mc.count() != 0:
            chatroom = mc[0]
        else:
            mc = target.chats.filter(target=me, is_dm=True)
            if mc.count() != 0:
                chatroom = mc[0]
            else:
                chatroom = ChatRoom.objects.create(name="dm_"+me.name+"_"+target.name, creator=me,
                                                   created_time=timezone.now(), location=me.location,
                                                   is_dm=True, target=target)

                Member_ChatRoom.objects.create(member=me, chat_room=chatroom, member_timestamp=timezone.now())
                Member_ChatRoom.objects.create(member=target, chat_room=chatroom, member_timestamp=timezone.now())
        return render(request, 'Chat/room.html',
                      {'room_name': chatroom.pk, 'member_pk': me.pk})
