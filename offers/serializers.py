from django.utils import timezone

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from helpers.dates import Date

from .models import Offer, Discount, Category


class OfferSerializer(serializers.ModelSerializer):
    publisher = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    def get_publisher(self, obj=None):
        ret = dict()
        # pass
        if obj:
            ret['name'] = str(obj.publisher.name)
            ret['image'] = "/media/" + str(obj.publisher.image)
            return ret

    def get_category(self, obj=None):
        ret = dict()
        if obj:
            ret['name'] = str(obj.category.name)
            return ret

    def get_days_remaining(self, obj):
        if obj:
            return Date.calculate_remaining_days(timezone.now(),
                                                 obj.end_date)

    class Meta:
        model = Offer
        # fields = "__all__"
        exclude = ('bending',)
