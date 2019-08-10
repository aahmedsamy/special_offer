from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.db.models import Count

from datetime import timedelta

from helpers.validators import HasSvgExtention, ImageOrVideo
from helpers.images import Image

from users.models import SearcherNotification, AdvertiserNotification

from .managers import (PendingManager, NotPendingManager)
# Create your models here.


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    image = models.ImageField(_("Image"), upload_to="categories/images/",)
    small_image_path = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class FollowedCategory(models.Model):
    searcher = models.ForeignKey("users.Searcher", verbose_name=_(
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
        unique_together = ('searcher', 'category')


class Offer(models.Model):
    PENDING = _("Pending")
    DECLINED = _("Declined")
    PUBLISHED = _("Published")
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (DECLINED, _("Declined")),
        (PUBLISHED, _("Published"))
    )
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
    status = models.CharField(
        _("Status"), max_length=50, choices=STATUS_CHOICES, default=PENDING)

    __original_status = PENDING

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        original_status = self.__original_status
        self.__original_status = self.status
        super().save(force_insert, force_update, *args, **kwargs)
        if self.status != original_status:
            if self.status == self.PUBLISHED:
                fcs = FollowedCategory.objects.filter(category=self.category)
                for fc in fcs:
                    SearcherNotification.objects.create(
                        offer=self, searcher=fc.searcher, status=self.status)
            AdvertiserNotification.objects.create(
                offer=self, advertiser=self.publisher, status=self.status)

    def __str__(self):
        return self.name

    def likes_count(self):
        return self.like_offer.count()

    likes_count.short_description = (_("Likes"))

    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")


class PendingOffer(Offer):

    objects = PendingManager()

    class Meta:

        proxy = True
        verbose_name = _("Pending Offer")
        verbose_name_plural = _("Pending Offers")


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
    PENDING = _("Pending")
    DECLINED = _("Declined")
    PUBLISHED = _("Published")
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (DECLINED, _("Declined")),
        (PUBLISHED, _("Published"))
    )
    publisher = models.ForeignKey("users.Publisher", verbose_name=_(
        "Publisher"), on_delete=models.CASCADE,
        related_name="publisher_discount")
    category = models.ForeignKey("offers.Category", verbose_name=_(
        "Category"), on_delete=models.PROTECT, null=True)
    name = models.CharField(_("Name"), max_length=256)
    description = models.TextField(_("Description"), max_length=1024)
    precentage = models.FloatField(_("Precentage"), validators=[
                                   MinValueValidator(0.0),
                                   MaxValueValidator(100.0)])
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))
    visited = models.PositiveIntegerField(_("Visited"), default=0)
    status = models.CharField(
        _("Status"), max_length=50, choices=STATUS_CHOICES, default=PENDING)

    __original_status = PENDING

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        original_status = self.__original_status
        self.__original_status = self.status
        super().save(force_insert, force_update, *args, **kwargs)
        if self.status != original_status:
            if self.status == self.PUBLISHED:
                fcs = FollowedCategory.objects.filter(category=self.category)
                for fc in fcs:
                    SearcherNotification.objects.create(
                        discount=self, searcher=fc.searcher, status=self.status)
            AdvertiserNotification.objects.create(
                discount=self, advertiser=self.publisher, status=self.status)

    def __str__(self):
        return self.name

    def likes_count(self):
        return self.like_discount.count()

    likes_count.short_description = (_("Likes"))

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")


class PendingDiscount(Discount):

    objects = PendingManager()

    class Meta:

        proxy = True
        verbose_name = _("Pending Discount")
        verbose_name_plural = _("Pending Discounts")


class Like(models.Model):
    searcher = models.ForeignKey("users.Searcher", verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='like_user')
    offer = models.ForeignKey("offers.Offer", verbose_name=_(
        "Offer"), on_delete=models.CASCADE, related_name='like_offer', null=True)
    discount = models.ForeignKey("offers.Discount", verbose_name=_(
        "Discount"), on_delete=models.CASCADE, related_name='like_discount', null=True)

    class Meta:
        verbose_name = _("Like")
        verbose_name = _("Likes")
        unique_together = ('searcher', 'offer', 'discount')


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


class Story(models.Model):
    PENDING = _("Pending")
    DECLINED = _("Declined")
    APPROVED = _("Approved")
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (DECLINED, _("Declined")),
        (APPROVED, _("Approved"))
    )
    advertiser = models.ForeignKey("users.Publisher", verbose_name=_(
        "Advertiser"), on_delete=models.CASCADE, related_name="advertiser_stories")
    media = models.FileField(
        _("Image/Video"), upload_to="stories/", max_length=256, validators=[ImageOrVideo])
    desc = models.TextField(_("Description"), max_length=1024)
    start_time = models.DateTimeField(_("Start date"))
    number_of_hours = models.PositiveSmallIntegerField(_("Number of hours"), validators=[
        MinValueValidator(1),
        MaxValueValidator(24)])
    status = models.CharField(
        _("Status"), max_length=50, choices=STATUS_CHOICES, default=PENDING)

    __original_status = PENDING

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
        ordering = ['-id']

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        original_status = self.__original_status
        self.__original_status = self.status
        self.end_time = self.start_time + timedelta(hours=self.number_of_hours)
        super().save(force_insert, force_update, *args, **kwargs)
        if self.status != original_status:
            AdvertiserNotification.objects.create(
                story=self, advertiser=self.advertiser, status=self.status)

    def get_end_date(self, hours):
        return self.start_time + timedelta(hours=hours)


class PendingStory(Story):

    objects = PendingManager()

    class Meta:

        proxy = True
        verbose_name = _("Pending Story")
        verbose_name_plural = _("Pending Stories")


def compress_offer_image(sender, instance, **kwargs):
    img = Image()
    for image in instance.offer_images.all():
        image.small_image_path = img.compress_image_tinify(image=image.image)
        image.save()


def compress_discount_image(sender, instance, **kwargs):
    img = Image()
    for image in instance.discount_images.all():
        image.small_image_path = img.compress_image_tinify(image=image.image)
        image.save()


# post_save.connect(compress_offer_image, sender=Offer)
# post_save.connect(compress_discount_image, sender=Discount)
