from django.db import models


class TransactionManager(models.Manager):

    def get_queryset(self):

        return super(TransactionManager, self).get_queryset().filter(

            status=self.PAID)
