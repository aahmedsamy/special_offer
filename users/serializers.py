from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from offers.serializers import (OfferSerializer, DiscountSerializer, StorySerializer)

from .models import User, Searcher, Publisher, SearcherNotification, AdvertiserNotification

class SearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Searcher
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    trading_doc = Base64ImageField()

    class Meta:
        model = Publisher
        exclude = ['phone_verified', 'phone_verification_code']

class UserSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    publisher = PublisherSerializer(read_only=True)
    searcher = SearcherSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'searcher', 'publisher', 'likes')
    
    def get_likes(self, obj):
        if obj and obj.is_searcher():
            return obj.searcher.get_liked_ads()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=265)
    password1 = serializers.CharField(max_length=265)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'searcher', 'publisher', 'password', 'password1')

    def validate(self, data):
        """
        Validate if password and password1 are identical.
        """
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                "'password' and 'password1' fields aren't the same!")
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password1 = serializers.CharField(max_length=20)

    def validate(self, data):
        """
        Validate if password and password1 are identical.
        """
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                "'password' and 'password1' fields aren't the same!")
        return data


class PasswordResetingSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    pass_reset_code = serializers.CharField(max_length=7)
    password = serializers.CharField(max_length=255)
    password1 = serializers.CharField(max_length=20)

    def validate(self, data):
        """
        Validate if password and password1 are identical.
        """
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                "'password' and 'password1' fields aren't the same!")
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=20)


class VerficationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class SearcherNotificationSerializer(serializers.ModelSerializer):
    offer = OfferSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = SearcherNotification
        exclude = ['searcher']

class AdvertiserNotificationSerializer(serializers.ModelSerializer):
    offer = OfferSerializer()
    discount = DiscountSerializer()
    story = StorySerializer()
    class Meta:
        model = AdvertiserNotification
        exclude = ['advertiser']
    
    # def get_offer(self, obj):
    #     ret = dict()
    #     if obj.offer:
    #         ret['offer'] = obj.offer.name
    #         ret['category'] = obj.offer.category.name
    #         return ret
    
    # def get_discount(self, obj):
    #     ret = dict()
    #     if obj.discount:
    #         ret['discount'] = obj.discount.name
    #         ret['category'] = obj.discount.category.name
    #         return ret
