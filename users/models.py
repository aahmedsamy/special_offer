from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as u

from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    NORMAL = 100
    PREMUIM = 101
    USER_TYPE_CHOICES = (
        (NORMAL, _('Normal')),
        (PREMUIM, _('Premuim'))
    )
    name = models.CharField(_('Name'), max_length=255)
    user_type = models.SmallIntegerField(
        choices=USER_TYPE_CHOICES, default=NORMAL)
    email = models.EmailField(_('Email address'), unique=True)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    verification_code = models.CharField(
        max_length=6, null=True, blank=True)
    verified = models.BooleanField(_("Verified"), default=False)
    pass_reset_code = models.CharField(max_length=7, null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to="users/images")
    """User model."""
    use_in_migrations = True
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    objects = UserManager()

    @property
    def total_visits(self):
        offer = self.publisher_offer.aggregate(Sum("visited"))['visited']
        discount = self.publisher_discount.aggregate(Sum("visited"))['visited']
        return offer + discount

    def is_verified(self):
        return self.verified

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Subscriptions(models.Model):
    pass
