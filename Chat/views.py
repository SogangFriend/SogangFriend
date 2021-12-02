import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import *

from .models import *
# Create your views here.


class ChatView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/chat/'

    def get(self, request):
        member_pk = request.session.get('member')
        member = Member.objects.get(pk=member_pk)
        rooms = Member_ChatRoom.objects.filter(member=member)
        return render(request, 'Chat/chat.html',
                      {'rooms': rooms, 'member_pk': member_pk})


class RoomCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/'

    def post(self, request):
        body = json.loads(request.body)
        name = body['name']
        member_pk = request.session.get('member')
        member = Member.objects.get(pk=member_pk)
        chatroom = ChatRoom.objects.create(name=name, creator=member,
                                           created_time=timezone.now(), location=member.location)
        Member_ChatRoom.objects.create(member=member, chat_room=chatroom, member_timestamp=timezone.now())
        data = {'message': "<div class='swal-confirm-sent'>채팅방이 생성되었습니다.</div>"}

        return JsonResponse(data)


class EnterChatView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = "/"

    def post(self, request):
        body = json.loads(request.body)
        room_pk = body['room_pk']
        member_pk = request.session.get('member')
        member = Member.objects.get(pk=member_pk)
        chatroom = ChatRoom.objects.get(pk=room_pk)
        data = {'new': True, 'room_pk': room_pk}
        if Member_ChatRoom.objects.filter(member=member, chat_room=chatroom).count() == 0:
            Member_ChatRoom.objects.create(member=member, chat_room=chatroom, member_timestamp=timezone.now())
            request.session['default'] = room_pk
            return redirect('/chat/')
        else:
            data['new'] = False
            return JsonResponse(data)


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
            if room.member_timestamp < room.chat_room.timestamp:
                room.unread = True
                room.save()
                flag = True
        ret = {'unread': flag}

        return JsonResponse(ret)


class RoomView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, room_pk):
        return render(request, "Chat/chat_room.html", {"room_pk": room_pk})


class MessagesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, room_pk):
        chatroom = ChatRoom.objects.get(pk=room_pk)
        msgs = Message.objects.filter(chat_room=chatroom)
        msgs = list(msgs.values())
        return JsonResponse(msgs, safe=False)
