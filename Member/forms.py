from django import forms


class MailForm(forms.Form):
    email = forms.CharField(label="Email", max_length=100)
