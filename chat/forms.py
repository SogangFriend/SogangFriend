from django import forms


class ChatRoomForm(forms.Form):
    NickName = forms.CharField(label='Nick Name', max_length=50)
    Room_Name = forms.CharField(label='Room Name', max_length=100)