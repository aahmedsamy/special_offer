from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as u

from .managers import UserManager
# Create your models here.


class User(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('First name'), max_length=256)
    phone = models.CharField(_('Phone'), max_length=20, unique=True)
    verification_code = models.CharField(max_length=4, null=True, blank=True)
    verified = models.BooleanField(_("Verified"), default=False)
    pass_reset_code = models.CharField(max_length=7, null=True, blank=True)

    """User model."""
    use_in_migrations = True
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    objects = UserManager()
    
    def is_verified(self):
        return self.verified
    
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")