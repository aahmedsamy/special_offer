from django.utils import timezone

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from helpers.dates import Date
from helpers.images import Image

from galleries.serializers import OfferImageSerializer, DiscountImageSerializer
from galleries.models import OfferImage, DiscountImage

from .models import (Offer, Discount, Category,
                     OfferAndDiscountFeature, PlusItem, OfferAndDiscountFeature, Like, Story)


class PlusItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlusItem
        fields = '__all__'
        read_only_fields = ('offer',)


class OfferAndDiscountFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferAndDiscountFeature
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    plus_offer = PlusItemSerializer(many=True)
    offer_images = OfferImageSerializer(many=True)
    offer_features = OfferAndDiscountFeatureSerializer(many=True, )
    publisher = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

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

    def get_likes(self, obj):
        return obj.likes_count()

    class Meta:
        model = Offer
        # fields = "__all__"
        exclude = ('status',)
        read_only_fields = ('visited', 'publisher')

    def create(self, validated_data):
        request = self.context.get("request", None)
        advertiser = request.user.publisher
        images_data = validated_data.pop('offer_images')
        plus_items = validated_data.pop('plus_offer')
        features = validated_data.pop('offer_features')
        print(validated_data)
        offer = Offer.objects.create(publisher=advertiser, **validated_data)

        room_images = []
        for image in images_data:
            room_images.append(
                OfferImage.objects.create(offer=offer, **image))
        Image.compress_list_of_images(room_images)

        for item in plus_items:
            PlusItem.objects.create(offer=offer, **item)

        for feature in features:
            OfferAndDiscountFeature.objects.create(offer=offer, **feature)

        return offer


class DiscountPostSerializer(serializers.ModelSerializer):
     class Meta:
        model = Discount
        # fields = "__all__"
        exclude = ('status', 'visited')


class DiscountSerializer(serializers.ModelSerializer):
    discount_images = DiscountImageSerializer(many=True,)
    discount_features = OfferAndDiscountFeatureSerializer(many=True, )
    publisher = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

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

    def get_days_remaining(self, obj):
        if obj:
            return Date.calculate_remaining_days(timezone.now(),
                                                 obj.end_date)

    def get_likes(self, obj):
        return obj.likes_count()

    class Meta:
        model = Discount
        # fields = "__all__"
        exclude = ('status',)
        read_only_fields = ('visited', 'publisher')

    def create(self, validated_data):
        request = self.context.get("request", None)
        advertiser = request.user.publisher
        images_data = validated_data.pop('discount_images')
        features = validated_data.pop('discount_features')
        discount = Discount.objects.create(
            publisher=advertiser, **validated_data)

        room_images = []
        for image in images_data:
            room_images.append(
                DiscountImage.objects.create(discount=discount, **image))
        Image.compress_list_of_images(room_images)

        for feature in features:
            OfferAndDiscountFeature.objects.create(
                discount=discount, **feature)

        return discount


class CategorySerializer(serializers.ModelSerializer):
    small_image_path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('small_image_path',)

    def get_small_image_path(self, obj):
        request = self.context.get("request", None)
        return request.build_absolute_uri(
            obj.small_image_path) if obj.small_image_path else ''


class LikeOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['offer', 'searcher']


class LikeDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['discount', 'searcher']


class StorySerializer(serializers.ModelSerializer):
    advertiser_data = serializers.SerializerMethodField()

    def get_advertiser_data(self, obj=None):
        ret = dict()
        request = self.context['request']
        # pass
        if obj:
            ret['name'] = str(obj.advertiser.name)
            if obj.advertiser.image:
                ret['image'] = request.build_absolute_uri(
                    obj.advertiser.image.url)
            return ret

    class Meta:
        model = Story
        # fields = "__all__"
        exclude = ('status',)
        read_only_fields = ('advertiser_data', 'end_time',)

