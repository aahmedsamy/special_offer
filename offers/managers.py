from django.db import models


class BendingManager(models.Manager):

    def get_queryset(self):

        return super(BendingManager, self).get_queryset().filter(

            bending=True)


class NotBendingManager(models.Manager):

    def get_queryset(self):

        return super(BendingManager, self).get_queryset().filter(

            bending=False)
