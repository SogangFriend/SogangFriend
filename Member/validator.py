from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    """
    custom password validator
    """

    def __init__(self, min_length=7):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("비밀번호는 최소 %(min_length)d 자 이상이어야 합니다."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('숫자를 포함해야 합니다.'))
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('영문자를 포함해야 합니다.'))

    def get_help_text(self):
        return _(
            "비밀번호는 7자 이상의 영문자가 숫자가 혼합되어야 합니다."
        )

