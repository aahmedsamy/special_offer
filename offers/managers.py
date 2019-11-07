from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

# from offers.models import Offer

class PendingManager(models.Manager):

    def get_queryset(self):

        return super(PendingManager, self).get_queryset().filter(

            status=_("Pending"))


class NotPendingManager(models.Manager):

    def get_queryset(self):

        return super(NotPendingManager, self).get_queryset().filter(

            ~Q(status=_("Pending")))
