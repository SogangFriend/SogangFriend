from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = 'username'

    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        username = cleaned_data.get('username')
        if ('@', '.', '-', '+') in username:
            self.add_error('username', 'Symbols @/./-/+ are not allowed in username.')
        return cleaned_data


# same for UserChangeForm
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Member
        fields = 'username'
        # Removed email field. Anyone won't want to change email after registering. Go as you like.

    def clean(self):
        cleaned_data = super(CustomUserChangeForm, self).clean()
        username = cleaned_data.get('username')
        if ('@', '.', '-', '+') in username:
            self.add_error('username', 'Symbols @/./-/+ are not allowed in username.')
        return cleaned_data
