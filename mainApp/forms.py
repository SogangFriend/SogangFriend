from django import forms


class TestForm(forms.Form):
    location = forms.CharField(label='Location', max_length=50)