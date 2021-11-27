from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import *
from channels.db import database_sync_to_async

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

        return redirect('/chat/')

      
class ChatView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/'

    def get(self, request):
        member_pk = request.session.get('member')
        member = Member.objects.get(pk=member_pk)
        rooms = Member_ChatRoom.objects.filter(member=member)
        return render(request, 'Chat/chat_test.html',
                      {'rooms': rooms, 'member_pk': member_pk})


class EnterChatView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/'

    def get(self, request, room):
        member_pk = request.session.get('member')
        member = Member.objects.get(pk=member_pk)
        chat_room = ChatRoom.objects.get(pk=room)
        mc = Member_ChatRoom.objects.filter(member=member, chat_room=chat_room)
        if mc.count() == 0:
            Member_ChatRoom.objects.create(member=member, chat_room=chat_room,
                                           member_timestamp=timezone.now())
        else:
            mc[0].unread = False
        return redirect('/chat/')


class EnterDMView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/'

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


class CheckUnreadView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        member_pk = request.session['member']

        member = Member.objects.get(pk=member_pk)

        rooms = Member_ChatRoom.objects.filter(member=member)
        flag = False
        for room in rooms:
            if room.member_timestamp > room.chat_room.timestamp:
                room.unread = True
                room.save()
                flag = True
        ret = {'unread': flag}

        return JsonResponse(ret)

