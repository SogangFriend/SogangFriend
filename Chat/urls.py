from django.urls import path
from .views import *
app_name = 'Chat'

urlpatterns = [
    path('', ChatView.as_view(), name='home'),
    path('new/', RoomCreateView.as_view(), name='new'),
    path('dm/<str:pk>/', EnterDMView.as_view(), name='dm'),
    # ajax 통신 url
    path('enter/', EnterChatView.as_view(), name='enter'),
    path('unread/', CheckUnreadView.as_view(), name='check'),
]
