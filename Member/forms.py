from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import SetPasswordForm
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


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        fields = ['email']

    def __init__(self, *args, **kwarg):
        super(EmailForm, self).__init__(*args, **kwarg)
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_email',
        })


class AuthNumForm(forms.Form):
    auth_num = forms.CharField(widget=forms.TextInput)

    class Meta:
        fields = ['auth_num']

    def __init__(self, *args, **kwargs):
        super(AuthNumForm, self).__init__(*args, **kwargs)
        self.fields['auth_num'].label = '인증번호'
        self.fields['auth_num'].widget.attrs.update({
            'class': 'form-control',
            'id': 'auth_num',
        })


class PasswordResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = "새 비밀번호"
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['new_password2'].label = "새 비밀번호 확인"
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control'
        })


class EditProfileView(forms.Form):
    profile_photo = forms.ImageField(label="이미지", required=False)
    name = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)
    location = forms.CharField()
    introduction = forms.CharField(widget=forms.TextInput)

    # password = forms.

    class Meta:
        fields = ['profile_photo', 'name', 'email', 'location', 'introduction']

    def __init__(self, *args, **kwargs):
        super(EditProfileView, self).__init__(*args, **kwargs)
        self.fields['name'].label = "닉네임"
        self.fields['name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['email'].label = "이메일"
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'readonly': 'True'
        })
        self.fields['location'].label = "지역"
        self.fields['location'].widget.attrs.update({
            'class': 'form-control',
            'readonly': 'True'
        })
        self.fields['introduction'].label = "자기소개"
        self.fields['introduction'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['profile_photo'].label = ""
        self.fields['profile_photo'].widget.attrs.update({
            'class': 'form-control'
        })
