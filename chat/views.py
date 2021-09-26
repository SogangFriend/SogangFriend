from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *
from .forms import *
from .models import *
# Create your views here.


class ChatHomeView(View):
    def get(self, request):
        return render(request, 'chat/chat_home.html', {})


class RoomView(View):
    form_class = ChatRoomForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'chat/chat_form.html', {"form": form})

    # def post(self, request): #room_name 중복확인, nickname 중복확인?
    #     room_name = request.POST.get('room_name', '')
    #     member = request.POST.get('member', '')
    #     nick_name = request.POST.get('nick_name','')
    #
    #     res_data = {}
    #     if not room_name:
    #         res_data['error'] = "Room Name을 입력해 주세요."
    #
    #     elif not nick_name:
    #         res_data['error'] = "Nickname을 입력해 주세요."
    #
    #     else:
    #         return render(request, 'chat/room.html')
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





