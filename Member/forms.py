from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Member


class MemberCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('email', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        member = super().save(commit=False)
        member.set_password(self.cleaned_data["password1"])
        if commit:
            member.save()
        return member


class MemberChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        fields = ('email', 'password', 'name',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)

#class ProfileUpdateForm(forms.ModelForm):
#    profile_image = forms.ImageField(required=False)

 #   class Meta:
#        model = Member
#        fields = ['intro','profile_image']

#        widgets = {
#            'intro': forms.TextInput(attrs={'class': 'form-control'}),
#            'profile_image' : forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'readURL(this);'}),
#        }

#        labels = {
 #           'profile_image': '프로필 사진',
#            'intro': '인사말',
 #       }