from django.db import models
from Member.models import *
from django.utils import timezone
# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, null=False)
    creator = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False, related_name='my_chatrooms')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    created_time = models.DateTimeField()
    timestamp = models.DateTimeField(default=timezone.now) # 가장 최신의 채팅 시간
    '''participants가 있어야 함'''
    participants = models.ManyToManyField(Member, through='Member_ChatRoom', related_name='chats')
    is_dm = models.BooleanField(default=False)
    target = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, default=None)


class Member_ChatRoom(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    member_timestamp = models.DateTimeField() # 멤버가 나간 시간 -> develop : 멤버가 지금 채팅방에 머물지 않고 있을 때
    unread = models.BooleanField(default=False)


class Message(models.Model):
    message = models.TextField(null=False, blank=False)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=False, blank=False)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False, related_name='my_messages')
    sender_name = models.CharField(max_length=30, default=sender.name)
    timestamp = models.DateTimeField()

