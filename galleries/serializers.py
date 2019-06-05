from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from .models import (OfferImage, DiscountImage,)


class OfferImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = OfferImage
        fields = '__all__'
        read_only_fields = ('small_image_path',)


class DiscountImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = DiscountImage
        fields = '__all__'
        read_only_fields = ('small_image_path',)
