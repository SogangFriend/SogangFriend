from django.db import models
from Member.models import *
# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, null=False)
    creator = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False)
    created_time = models.DateTimeField()
    '''participants가 있어야 함'''

