from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import Publisher

from .managers import TransactionManager
# Create your models here.


class TransactionAttempt(models.Model):
    CREATED = 100
    CANCELD = 101
    PAID = 102
    STATUS_CHOICES = (
        (CREATED, _("Created")),
        (CANCELD, _("Canceled")),
        (PAID, _("Paid"))
    )
    advertiser = models.ForeignKey(Publisher, verbose_name=_(
        "Advertiser"), on_delete=models.PROTECT, )
    payment_id = models.CharField(
        _("Payment ID"), max_length=256, editable=False, null=True, db_index=True)
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=STATUS_CHOICES, default=CREATED)
    amount = models.FloatField(_("Amount"))
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True)
    created_at = models.DateTimeField(
        verbose_name=_("Created at"), auto_now_add=True)
    message = models.TextField(_("Message"), null=True)


class Transaction(TransactionAttempt):

    objects = TransactionManager()

    class Meta:

        proxy = True
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
