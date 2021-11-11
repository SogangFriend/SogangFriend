from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    """
    custom password validator
    """

    def validate(self, password, user=None):
        if len(password) == 0:
            raise ValidationError(_("Your password can't be an empty string."))

    def get_help_text(self):
        return _("Your password can't be an empty string.")

