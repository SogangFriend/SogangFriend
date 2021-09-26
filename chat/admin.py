from django.contrib import admin
from .models import ChatRoom, Member_ChatRoom, Message
# Register your models here.
# class TaskInline(admin.TabularInline):
#     model = Message
#     extra = 3
#
# class RoomAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ("ChatRoom", {'fields': ['room_name']}),
#     ]
#     inlines = [TaskInline]

#
# admin.site.register(ChatRoom, RoomAdmin)