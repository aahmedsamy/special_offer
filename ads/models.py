from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# Create your models here.


class Ad(models.Model):
    TOP = 'Top'
    BUTTOM = 'Buttom'
    POSITION_CHOICES = [
        (TOP, _('Top')),
        (BUTTOM, _('Buttom'))
    ]
    advertiser = models.ForeignKey("users.Publisher", verbose_name=_(
        "Advertiser"), on_delete=models.CASCADE)
    offer = models.ForeignKey("offers.Offer", verbose_name=_("Offer"),
                              on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey("offers.Discount", verbose_name=_("Discount"),
                                 on_delete=models.CASCADE, null=True,
                                 blank=True)
    name = models.CharField(_("Name"), max_length=256)
    image = models.ImageField(_("Ad Image"), upload_to='ads/images')
    position = models.CharField(
        _("Position"), max_length=256, choices=POSITION_CHOICES)
    period = models.PositiveSmallIntegerField(
        _("Period"), help_text=_("Please set ad period in seconds."))
    start_date = models.DateField(
        _("Start date"), help_text=_("Start viewing date"))
    end_date = models.DateField(_("End date"), help_text=_("End viewing date"))

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                _('End date must be greater than Start date.'))

        if not self.offer and not self.discount:
            raise ValidationError(_('Please select offer or discount.'))

        if self.offer and self.discount:
            raise ValidationError(
                _('It is not allowed to select offer and discount for the same Ad.'))

    class Meta:
        verbose_name = _("Ad")
        verbose_name_plural = _("Ads")
