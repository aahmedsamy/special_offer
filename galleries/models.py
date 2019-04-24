from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class OfferImage(models.Model):
    offer = models.ForeignKey(
        "offers.Offer", on_delete=models.CASCADE, related_name="offer_image")
    image = models.ImageField(_("Image"), upload_to="items/imags/")

    class Meta:
        verbose_name = _("Offer image")
        verbose_name_plural = _("Offer images")


class PlusItemImage(models.Model):
    plus_item = models.ForeignKey(
        "offers.PlusItem", on_delete=models.CASCADE,
        related_name="plus_item_image")
    image = models.ImageField(_("Image"), upload_to="items/imags/")

    class Meta:
        verbose_name = _("Offer image")
        verbose_name_plural = _("Offer images")


class DiscountImage(models.Model):
    discount = models.ForeignKey(
        "offers.Discount", on_delete=models.CASCADE,
        related_name="discount_image")
    image = models.ImageField(_("Image"), upload_to="items/imags/")

    class Meta:
        verbose_name = _("Offer image")
        verbose_name_plural = _("Offer images")
