from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response

from helpers.permissions import (IsPublisher, IsVerified)
from helpers.images import Image

from offers.models import Offer, Discount

from .models import OfferImage, DiscountImage
from .serializers import (OfferImageSerializer, DiscountImageSerializer)

# Create your views here.

def compress_list_of_images(images):
    for image in images:
        # img = Image()
        image.small_image_path = Image.compress_image_tinify(image.image)
        image.save()

class OfferImageViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):

    # queryset = Offer.objects.all()

    serializer_class = OfferImageSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create']:
            permission_classes = [IsPublisher, IsVerified]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request):
        context = dict()
        required_fields = ['offer', 'images']
        error = False
        for key in required_fields:
            if key not in request.data.keys():
                error = True
                context[key] = "This field is required."
        if error:
            return Response(context, 400)
        offer_id = request.data['offer']
        offers = Offer.objects.filter(publisher=request.user.publisher)
        get_object_or_404(offers, pk=offer_id)
        for i in range(len(request.data['images'])):
            request.data['images'][i]['offer'] = offer_id
        serializer = OfferImageSerializer(
            data=request.data['images'], many=True)
        if serializer.is_valid():
            images = serializer.save()
            Image.compress_list_of_images(images)
            context['detail'] = "Images uploaded successfully."
            return Response(context)
        else:
            return Response(serializer.errors, 400)


class DiscountImageViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):

    # queryset = Discount.objects.all()

    serializer_class = DiscountImageSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create']:
            permission_classes = [IsPublisher, IsVerified]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request):
        context = dict()
        required_fields = ['discount', 'images']
        error = False
        for key in required_fields:
            if key not in request.data.keys():
                error = True
                context[key] = "This field is required."
        if error:
            return Response(context, 400)
        discount_id = request.data['discount']
        discounts = Discount.objects.filter(publisher=request.user.publisher)
        get_object_or_404(discounts, pk=discount_id)
        for i in range(len(request.data['images'])):
            request.data['images'][i]['discount'] = discount_id
        serializer = DiscountImageSerializer(
            data=request.data['images'], many=True)
        if serializer.is_valid():
            images = serializer.save()
            Image.compress_list_of_images(images)
            context['detail'] = "Images uploaded successfully."
            return Response(context)
        else:
            return Response(serializer.errors, 400)
