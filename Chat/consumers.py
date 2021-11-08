from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.member = self.scope['url_route']['kwargs']['member_pk']
        # if self.scope['url_route']['kwargs']['room_name']로 된 이름이나 뭐 그런거가
        # 디비에 없을 경우 방 못 들어감
        self.room_group_name = 'chat_%s' % self.room_name

        await self.enter_chatroom()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        mc = await self.get_member_chatroom()
        await self.set_member_timestamp(mc)

        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )

    #receive message from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_pk = text_data_json['sender']
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'sender': sender_pk
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_pk = event['sender']
        sender = await self.get_member_with_pk(sender_pk)
        msg = await self.create_message(message)
        await self.set_chat_room_timestamp()
        # member = await self.get_member()
        await self.send(text_data=json.dumps({
            'sender' : sender.name,
            'message' : message,
            'timestamp' : msg.timestamp
        }, default=str))

    @database_sync_to_async
    def get_member(self):
        return Member.objects.get(pk=self.member)

    @database_sync_to_async
    def get_member_with_pk(self, pk):
        return Member.objects.get(pk=pk)

    @database_sync_to_async
    def create_message(self, message):
        member = Member.objects.get(pk=self.member)
        chat_room = ChatRoom.objects.get(pk=self.room_name)
        msg = Message.objects.create(message=message, sender=member, chat_room=chat_room, timestamp=timezone.now())
        return msg

    @database_sync_to_async
    def set_chat_room_timestamp(self):
        chat_room = ChatRoom.objects.get(pk=self.room_name)
        chat_room.timestamp = timezone.now()
        chat_room.save()

    @database_sync_to_async
    def enter_chatroom(self):
        member = Member.objects.get(pk=self.member)
        chat_room = ChatRoom.objects.get(pk=self.room_name)
        if Member_ChatRoom.objects.filter(member=member, chat_room=chat_room).count() == 0:
            Member_ChatRoom.objects.create(member=member, chat_room=chat_room,
                                           member_timestamp=timezone.now())

    @database_sync_to_async
    def get_member_chatroom(self):
        member = Member.objects.get(pk=self.member)
        room = ChatRoom.objects.get(pk=self.room_name)
        return Member_ChatRoom.objects.get(member=member, Chat_room=room)

    @database_sync_to_async
    def set_member_timestamp(self, mc):
        mc.member_timestamp = timezone.now()
        mc.save()
