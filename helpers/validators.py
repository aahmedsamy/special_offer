from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class StringBaseValidator:
    message = _('Ensure all letters in this value is in english letters \
        (a:z and/or A:Z).')
    code = 'lower_uppercase'

    def __init__(self, value):
        cleaned = self.clean(value)
        params = {'code': self.code, 'show_value': cleaned, 'value': value}
        if self.check(cleaned):
            raise ValidationError(self.message, code=self.code, params=params)

    def check(self, value):
        value = value.lower()
        for i in value:
            if i < 'a' or i > 'z':
                return True

    def clean(self, x):
        return x


@deconstructible
class EnglishLowercaseValidator(StringBaseValidator):
    message = _('Ensure all letters in this value is in lowercase english \
         letters (a:z).')
    code = 'lowercase'

    def check(self, value):
        for i in value:
            if i < 'a' or i > 'z':
                return True


@deconstructible
class EnglishUppercaseValidator(StringBaseValidator):
    message = _('Ensure all letters in this value is in uppercase english \
        letters (A:Z).')
    code = 'upercase'

    def check(self, value):
        for i in value:
            if i < 'A' or i > 'Z':
                return True


@deconstructible
class HasSvgExtention(StringBaseValidator):
    message = "Please upload a SVG file"
    code = 'not_svg'

    def check(self, value):
        ext = value.name.split('.')[-1]
        if ext.lower() != "svg":
            return True