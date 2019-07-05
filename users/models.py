from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as u
from django.utils import timezone

from .managers import UserManager

import datetime

# Create your models here.


class User(AbstractUser):
    searcher = models.OneToOneField(
        "users.Searcher", on_delete=models.CASCADE, related_name="searcher",
        null=True, blank=True)
    publisher = models.OneToOneField(
        "users.Publisher", on_delete=models.CASCADE, related_name="publisher",
        null=True, blank=True)
    email = models.EmailField(_('Email address'), unique=True)
    verification_code = models.CharField(
        max_length=6, null=True, blank=True)
    verified = models.BooleanField(_("Verified"), default=False)
    pass_reset_code = models.CharField(max_length=7, null=True, blank=True)
    """User model."""
    use_in_migrations = True
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def is_verified(self):
        return True if self.verified else False

    def is_publisher(self):
        return True if self.publisher else False

    def is_searcher(self):
        return True if self.searcher else False

    def has_trading_doc(self):
        return True if self.trading_doc else False

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Searcher(models.Model):
    name = models.CharField(_('Searcher name'), max_length=255)

    def following_count(self):
        return self.followed_category_user.count()

    def email(self):
        return self.searcher.email

    def date_joined(self):
        return self.searcher.date_joined.strftime('(%d/%m/%Y) - (%H:%M:%S)')

    def last_login(self):
        ret = self.searcher.last_login.strftime('(%d/%m/%Y) - (%H:%M:%S)')
        return ret if ret else '-'

    def get_liked_ads(self):
        ret = dict()
        ret['offers'] = []
        ret['discounts'] = []
        likes = self.like_user.all().values('offer_id', 'discount_id')
        for like in likes:
            if like['offer_id']:
                ret['offers'].append(like["offer_id"])
            if like['discount_id']:
                ret['discounts'].append(like["discount_id"])
        return ret

    following_count.short_description = (_("Following count"))
    email.short_description = (_("Email"))
    date_joined.short_description = (_("Date joined"))
    last_login.short_description = (_("Last login"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Searcher")
        verbose_name_plural = _("Searchers")


class Publisher(models.Model):
    holidays = models.CharField(
        _("Holidays"), blank=True, max_length=256, null=True)
    name = models.CharField(_('Publisher name'), max_length=255)
    phone = models.CharField(_('Phone'), max_length=20)
    image = models.ImageField(_("Image"), upload_to="users/images")
    address_url = models.URLField(_("Address URL"), max_length=256, null=True)
    website_url = models.URLField(_("Website URL"), max_length=256, null=True)
    facebook_url = models.URLField(
        _("Facebook URL"), max_length=256, null=True)
    twitter_url = models.URLField(_("Twitter URL"), max_length=256, null=True)
    instgram_url = models.URLField(
        _("Instgram URL"), max_length=256, null=True)
    trading_doc = models.ImageField(
        _("Trading document"), upload_to="images/docs")
    work_start_at = models.TimeField(_("Work starts at"))
    work_end_at = models.TimeField(_("Work ends at"))

    def active_posts(self):
        pass

    def total_visits(self):
        offer = self.publisher_offer.aggregate(Sum("visited"))['visited__sum']
        offer = offer if offer else 0
        discount = self.publisher_discount.aggregate(Sum("visited"))[
            'visited__sum']
        discount = discount if discount else 0
        return offer + discount

    def likes(self):
        cnt = 0
        offers = self.publisher_offer.all()
        for offer in offers:
            cnt += offer.likes_count()

        discounts = self.publisher_discount.all()
        for discount in discounts:
            cnt += discount.likes_count()
        return cnt

    def active_posts_cnt(self):
        offers = self.publisher_offer.filter(start_date__lte=timezone.now(
        ), end_date__gte=timezone.now()).count()
        discounts = self.publisher_discount.filter(start_date__lte=timezone.now(
        ), end_date__gte=timezone.now()).count()
        return offers + discounts

    def email(self):
        return self.publisher.email

    def date_joined(self):
        return self.publisher.date_joined.strftime('(%d/%m/%Y) - (%H:%M:%S)')

    def last_login(self):
        ret = self.publisher.last_login.strftime('(%d/%m/%Y) - (%H:%M:%S)')
        return ret if ret else '-'

    def verified(self):
        return _("Verified") if self.publisher.is_verified() else _("Not verified")

    active_posts.short_description = (_("Active posts"))
    total_visits.short_description = (_("Total visits"))
    likes.short_description = (_("Likes"))
    email.short_description = (_("Email"))
    date_joined.short_description = (_("Date joined"))
    last_login.short_description = (_("Last login"))
    verified.short_description = (_("Verified"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")


class SearcherNotification(models.Model):
    searcher = models.ForeignKey("users.Searcher", verbose_name=_(
        "Searcher"), on_delete=models.CASCADE, related_name="searcher_notifications")
    offer = models.ForeignKey("offers.Offer", verbose_name=_(
        "Offer"), on_delete=models.CASCADE, related_name="offer_searcher_notifications", null=True)
    discount = models.ForeignKey("offers.Discount", verbose_name=_(
        "Discount"), on_delete=models.CASCADE, related_name="discount_searcher_notifications", null=True)
    
    status = models.CharField(_("Status"), max_length=50)

    class Meta:
        ordering = ['-id']


class AdvertiserNotification(models.Model):
    advertiser = models.ForeignKey("users.Publisher", verbose_name=_(
        "Advertiser"), on_delete=models.CASCADE, related_name="advertiser_notifications")
    offer = models.ForeignKey("offers.Offer", verbose_name=_(
        "Offer"), on_delete=models.CASCADE, related_name="offer_advertiser_notifications", null=True)
    discount = models.ForeignKey("offers.Discount", verbose_name=_(
        "Discount"), on_delete=models.CASCADE, related_name="discount_advertiser_notifications", null=True)
    
    status = models.CharField(_("Status"), max_length=50)
        

    class Meta:
        ordering = ['-id']
        verbose_name = _("AdvertiserNotification")
        verbose_name_plural = _("AdvertiserNotifications")
