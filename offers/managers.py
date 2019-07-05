from django.db import models
from django.db.models import Q

# from offers.models import Offer

class BendingManager(models.Manager):

    def get_queryset(self):

        return super(BendingManager, self).get_queryset().filter(

            status="Bending")


class NotBendingManager(models.Manager):

    def get_queryset(self):

        return super(BendingManager, self).get_queryset().filter(

            ~Q(status="Bending"))
