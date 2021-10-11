from django import forms


class ChatRoomForm(forms.Form):
    nick_name = forms.CharField(label='Nick Name', max_length=50)
    room_name = forms.CharField(label='Room Name', max_length=100)