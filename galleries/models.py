from django.db import models
# from django.db.models.singal import post_save
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from helpers.images import Image

# Create your models here.


class OfferImage(models.Model):
    offer = models.ForeignKey(
        "offers.Offer", on_delete=models.CASCADE, related_name="offer_images")
    image = models.ImageField(_("Image"), upload_to="items/imags/")
    small_image_path = models.TextField()

    # def clean(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image()
    #     self.small_image_path = img.compress_image_tinify(image=self.image)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Offer image")
        verbose_name_plural = _("Offer images")


class PlusItemImage(models.Model):
    plus_item = models.ForeignKey(
        "offers.PlusItem", on_delete=models.CASCADE,
        related_name="plus_item_image")
    image = models.ImageField(_("Image"), upload_to="items/imags/")
    small_image_path = models.TextField()

    # def clean(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image()
    #     self.small_image_path = img.compress_image_tinify(image=self.image)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Offer image")
        verbose_name_plural = _("Offer images")


class DiscountImage(models.Model):
    discount = models.ForeignKey(
        "offers.Discount", on_delete=models.CASCADE,
        related_name="discount_images")
    image = models.ImageField(_("Image"), upload_to="items/imags/")
    small_image_path = models.TextField()

    # def clean(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image()
    #     self.small_image_path = img.compress_image_tinify(image=self.image)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Offer image")
        verbose_name_plural = _("Offer images")


def compress_plus_item_image(sender, instance, **kwargs):
    img = Image()
    instance.small_image_path = img.compress_image_tinify(image=instance.image)
    instance.save()

post_save.connect(compress_plus_item_image, sender=PlusItemImage)
