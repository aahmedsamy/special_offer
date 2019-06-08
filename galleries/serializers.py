from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from .models import (OfferImage, DiscountImage,)


class OfferImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    small_image_path = serializers.SerializerMethodField()

    class Meta:
        model = OfferImage
        exclude = ('offer', )
        read_only_fields = ('small_image_path',)

    def get_small_image_path(self, obj):
        request = self.context.get("request", None)
        return request.build_absolute_uri(
            obj.small_image_path) if obj.small_image_path else ''


class DiscountImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    small_image_path = serializers.SerializerMethodField()

    class Meta:
        model = DiscountImage
        exclude = ('discount', )
        read_only_fields = ('small_image_path',)

    def get_small_image_path(self, obj):
        request = self.context.get("request", None)
        return request.build_absolute_uri(
            obj.small_image_path) if obj.small_image_path else ''
