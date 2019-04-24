from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (MinValueValidator, MaxValueValidator)

from helpers.validators import HasSvgExtention
# Create your models here.


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=256, unique=True)
    icon = models.FileField(_("Icon"), upload_to="icons/",
                            validators=[HasSvgExtention])

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Offer(models.Model):
    publisher = models.ForeignKey("users.User", verbose_name=_(
        "Publisher"), on_delete=models.CASCADE, related_name="publisher_offer")
    category = models.ForeignKey("offers.Category", verbose_name=_(
        "Category"), on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(_("Description"), max_length=1024)
    price = models.FloatField(_("Price"), validators=[MinValueValidator(0.0)])
    visited = models.PositiveIntegerField(_("Visited"), default=0)

    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")


class PlusItem(models.Model):
    offer = models.ForeignKey("offers.Offer", verbose_name=_(
        "Offer"), related_name="plus_offer", on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(_("Description"), max_length=1024)

    class Meta:
        verbose_name = _("Plus item")
        verbose_name_plural = _("Plus items")


class Discount(models.Model):
    publisher = models.ForeignKey("users.User", verbose_name=_(
        "Publisher"), on_delete=models.CASCADE,
        related_name="publisher_discount")
    category = models.ForeignKey("offers.Category", verbose_name=_(
        "Category"), on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(_("Description"), max_length=1024)
    price = models.FloatField(_("Price"), validators=[MinValueValidator(0.0)])
    visited = models.PositiveIntegerField(_("visited"), default=0)
    precentage = models.FloatField(_("Precentage"), validators=[
                                   MinValueValidator(0.0),
                                   MaxValueValidator(100.0)])

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")
