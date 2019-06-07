from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.db.models import Count

from helpers.validators import HasSvgExtention

from .managers import (BendingManager, NotBendingManager)
# Create your models here.


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=256, unique=True)
    image = models.ImageField(_("Image"), upload_to="categories/images/",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Offer(models.Model):
    publisher = models.ForeignKey("users.Publisher", verbose_name=_(
        "Publisher"), on_delete=models.CASCADE, related_name="publisher_offer")
    category = models.ForeignKey("offers.Category", verbose_name=_(
        "Category"), on_delete=models.PROTECT)
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(_("Description"), max_length=1024)
    price = models.FloatField(_("Price"), validators=[MinValueValidator(0.0)])
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))
    visited = models.PositiveIntegerField(_("Visited"), default=0)
    bending = models.BooleanField(_("Bending"), default=True)

    def __str__(self):
        return self.name

    def likes_count(self):
        return self.like_offer.count()

    likes_count.short_description = (_("Likes"))

    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")


class BendingOffer(Offer):

    objects = BendingManager()

    class Meta:

        proxy = True
        verbose_name = _("Bending Offer")
        verbose_name_plural = _("Bending Offers")


class PlusItem(models.Model):
    offer = models.ForeignKey("offers.Offer", verbose_name=_(
        "Offer"), related_name="plus_offer", on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Plus item")
        verbose_name_plural = _("Plus items")


class Discount(models.Model):
    publisher = models.ForeignKey("users.Publisher", verbose_name=_(
        "Publisher"), on_delete=models.CASCADE,
        related_name="publisher_discount")
    category = models.ForeignKey("offers.Category", verbose_name=_(
        "Category"), on_delete=models.PROTECT, null=True)
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(_("Description"), max_length=1024)
    price = models.FloatField(_("Price"), validators=[MinValueValidator(0.0)])
    precentage = models.FloatField(_("Precentage"), validators=[
                                   MinValueValidator(0.0),
                                   MaxValueValidator(100.0)])
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))
    visited = models.PositiveIntegerField(_("Visited"), default=0)
    bending = models.BooleanField(_("Bending"), default=True)

    def __str__(self):
        return self.name

    def likes_count(self):
        return self.like_discount.count()

    likes_count.short_description = (_("Likes"))

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")


class BendingDiscount(Discount):

    objects = BendingManager()

    class Meta:

        proxy = True
        verbose_name = _("Bending Discount")
        verbose_name_plural = _("Bending Discounts")


class Like(models.Model):
    user = models.ForeignKey("users.Searcher", verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='like_user')
    offer = models.ForeignKey("offers.Offer", verbose_name=_(
        "Offer"), on_delete=models.CASCADE, related_name='like_offer')
    discount = models.ForeignKey("offers.Discount", verbose_name=_(
        "Discount"), on_delete=models.CASCADE, related_name='like_discount')

    class Meta:
        verbose_name = _("Like")
        verbose_name = _("Likes")
        unique_together = ('user', 'offer', 'discount')


class FollowedCategory(models.Model):
    user = models.ForeignKey("users.Searcher", verbose_name=_(
        "User"), on_delete=models.CASCADE,
        related_name='followed_category_user')
    category = models.ForeignKey("offers.Category", verbose_name=_(
        "Category"), on_delete=models.CASCADE,
        related_name='followed_category_category')

    def __str__(self):
        return ""
        # return "{} --> {}".format(self.user.name, self.category.name)

    class Meta:
        verbose_name = _("Followed category")
        verbose_name_plural = _("Followed categories")
        unique_together = ('user', 'category')


class OfferAndDiscountFeature(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, verbose_name=_(
        "Offer"), related_name='offer_features')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, verbose_name=_(
        "Discount"), related_name='discount_features')
    name = models.CharField(_("Feature name"), max_length=256)
    desc = models.TextField(_("Description"), max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Offer and discount feature")
        verbose_name_plural = _("Offer and discount features")
