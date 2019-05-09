from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as u

from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    searcher = models.OneToOneField(
        "users.Searcher", on_delete=models.CASCADE, related_name="searcher",
        null=True, blank=True)
    publisher = models.OneToOneField(
        "users.Publisher", on_delete=models.CASCADE, related_name="publisher",
        null=True, blank=True)
    email = models.EmailField(_('Email address'), unique=True)
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    verification_code = models.CharField(
        max_length=6, null=True, blank=True)
    verified = models.BooleanField(_("Verified"), default=False)
    pass_reset_code = models.CharField(max_length=7, null=True, blank=True)
    """User model."""
    use_in_migrations = True
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    objects = UserManager()

    def total_visits(self):
        if self.user_type == self.NORMAL:
            return "--"
        offer = self.publisher_offer.aggregate(Sum("visited"))['visited__sum']
        offer = offer if offer else 0
        discount = self.publisher_discount.aggregate(Sum("visited"))[
            'visited__sum']
        discount = discount if discount else 0
        return offer + discount

    total_visits.short_description = (_("Total visits"))

    def is_verified(self):
        return self.verified

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Searcher(models.Model):
    name = models.CharField(_('Searcher name'), max_length=255)

    def following_count(self):
        return self.followed_category_user.count()

    following_count.short_description = (_("Following count"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Searcher")
        verbose_name_plural = _("Searchers")


class Publisher(models.Model):
    holidays = models.ManyToManyField(
        "users.Holiday", verbose_name=_("Holidays"), blank=True)
    name = models.CharField(_('Publisher name'), max_length=255)
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

    active_posts.short_description = (_("Active posts"))
    total_visits.short_description = (_("Total visits"))
    likes.short_description = (_("Likes"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")


class Subscriptions(models.Model):
        pass


class Holiday(models.Model):
    day = models.CharField(_("Day"), max_length=50)
