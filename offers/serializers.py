from django.utils import timezone

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from helpers.dates import Date

from galleries.serializers import OfferImageSerializer

from .models import (Offer, Discount, Category, OfferAndDiscountFeature)


class OfferPostSerializer(serializers.ModelSerializer):
     class Meta:
        model = Offer
        # fields = "__all__"
        exclude = ('bending', 'visited')


class OfferGetSerializer(serializers.ModelSerializer):
    publisher = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_publisher(self, obj=None):
        ret = dict()
        request = self.context['request']
        # pass
        if obj:
            ret['name'] = str(obj.publisher.name)
            if obj.publisher.image:
                ret['image'] = request.build_absolute_uri(
                    obj.publisher.image.url)
            return ret

    def get_category(self, obj=None):
        ret = dict()
        if obj:
            ret['name'] = str(obj.category.name)
            return ret

    def get_days_remaining(self, obj=None):
        if obj:
            return Date.calculate_remaining_days(timezone.now(),
                                                 obj.end_date)

    def get_images(self, obj=None):
        ret = []
        item = dict()
        request = self.context['request']
        if obj:
            images = obj.offer_image.all()
            for image in images:
                item = item.copy()
                item['image'] = request.build_absolute_uri(
                    image.image.url)
                if image.small_image_path:
                    item['small_image_path'] = request.build_absolute_uri(
                        image.small_image_path)
                ret.append(item)
        return ret

    class Meta:
        model = Offer
        # fields = "__all__"
        exclude = ('bending',)


class DiscountPostSerializer(serializers.ModelSerializer):
     class Meta:
        model = Discount
        # fields = "__all__"
        exclude = ('bending', 'visited')


class DiscountGetSerializer(serializers.ModelSerializer):
    publisher = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_publisher(self, obj=None):
        ret = dict()
        request = self.context['request']
        # pass
        if obj:
            ret['name'] = str(obj.publisher.name)
            if obj.publisher.image:
                ret['image'] = request.build_absolute_uri(
                    obj.publisher.image.url)
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

    def get_images(self, obj=None):
        ret = []
        item = dict()
        request = self.context['request']
        if obj:
            images = obj.discount_image.all()
            for image in images:
                item = item.copy()
                item['image'] = request.build_absolute_uri(
                    image.image.url)
                if image.small_image_path:
                    item['small_image_path'] = request.build_absolute_uri(
                        image.small_image_path)
                ret.append(item)
        return ret

    class Meta:
        model = Discount
        # fields = "__all__"
        exclude = ('bending',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OfferAndDiscountFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferAndDiscountFeature
        fields = '__all__'
    
