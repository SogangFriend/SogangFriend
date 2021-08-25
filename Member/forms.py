from django import forms


class MailForm(forms.Form):
    email = forms.CharField(label="email", max_length=100)
