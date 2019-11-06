from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from helpers.dates import Date
from helpers.images import Image

from users.models import Publisher

from galleries.serializers import OfferImageSerializer, DiscountImageSerializer
from galleries.models import OfferImage, DiscountImage

from .models import (Offer, Discount, Category,
                     OfferFeature, PlusItem, OfferFeature, Like, Story, StorySeen)


class PublisherSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    trading_doc = Base64ImageField()

    class Meta:
        model = Publisher
        exclude = ['phone_verification_code']


class PlusItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlusItem
        fields = '__all__'
        read_only_fields = ('offer',)


class OfferFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferFeature
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    plus_offer = PlusItemSerializer(many=True)
    offer_images = OfferImageSerializer(many=True)
    offer_features = OfferFeatureSerializer(many=True, )
    publisher = PublisherSerializer(read_only=True)
    days_remaining = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

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
        offer = Offer.objects.create(publisher=advertiser, **validated_data)

        room_images = []
        for image in images_data:
            room_images.append(
                OfferImage.objects.create(offer=offer, **image))
        # Image.compress_list_of_images(room_images)

        for item in plus_items:
            PlusItem.objects.create(offer=offer, **item)

        for feature in features:
            OfferFeature.objects.create(offer=offer, **feature)

        return offer


class DiscountPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        # fields = "__all__"
        exclude = ('status', 'visited')


class DiscountSerializer(serializers.ModelSerializer):
    discount_images = DiscountImageSerializer(many=True,)
    publisher = PublisherSerializer(read_only=True)
    days_remaining = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

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
        discount = Discount.objects.create(
            publisher=advertiser, **validated_data)

        room_images = []
        for image in images_data:
            room_images.append(
                DiscountImage.objects.create(discount=discount, **image))
        # Image.compress_list_of_images(room_images)

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
    advertiser = PublisherSerializer(read_only=True)

    class Meta:
        model = Story
        # fields = "__all__"
        exclude = ('status',)
        read_only = ['end_time']

    def create(self, validated_data):
        request = self.context.get("request", None)
        advertiser = request.user.publisher
        story = Story.objects.create(
            advertiser=advertiser, **validated_data)

        return story


class StoryOnlySerializer(serializers.ModelSerializer):
    # advertiser = PublisherSerializer(read_only=True)
    seen = serializers.SerializerMethodField()

    class Meta:
        model = Story
        # fields = "__all__"
        exclude = ('status',)
        read_only = ['end_time']

    def create(self, validated_data):
        request = self.context.get("request", None)
        advertiser = request.user.publisher
        story = Story.objects.create(
            advertiser=advertiser, **validated_data)

        return story

    def get_seen(self, obj):
        if not self.context['request'].user.is_anonymous and StorySeen.objects.filter(user=self.context['request'].user, story=obj).first():
            return True
        return False


class PublisherStoriesSerializer(serializers.ModelSerializer):
    advertiser_stories = serializers.SerializerMethodField()

    class Meta:
        model = Publisher
        fields = ('image', 'name', 'address',
                  'advertiser_stories', 'id')

    def get_advertiser_stories(self, obj):
        return StoryOnlySerializer(obj.advertiser_stories.filter(status=Story.APPROVED, start_time__lte=timezone.now(), end_time__gte=timezone.now()).order_by('start_time')
            , many=True, context=self.context).data
    # , start_time__lte = timezone.now(), end_time__gte = timezone.now()


class StorySeenSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySeen
        read_only_fields = ('user',)
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_anonymous:
            seen = StorySeen.objects.create(
                user=user, story=validated_data['story'])
            return seen
        else:
            raise ValidationError(
                _('Not logged in'))


class StorySerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Story
        # fields = "__all__"
        exclude = ('status',)
        read_only = ['end_time']
