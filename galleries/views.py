from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response

from helpers.permissions import IsPublisher

from offers.models import Offer, Discount

from .models import OfferImage, DiscountImage
from .serializers import (OfferImageSerializer, DiscountImageSerializer)

# Create your views here.


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
            permission_classes = [IsPublisher]
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
        offers = Offer.objects.filter(id=request.user.publisher.id)
        get_object_or_404(offers, pk=offer_id)
        for i in range(len(request.data['images'])):
            request.data['images'][i]['offer'] = offer_id
        serializer = OfferImageSerializer(
            data=request.data['images'], many=True)
        if serializer.is_valid():
            serializer.save()
            context['detail'] = "Images uploaded successfully."
            return Response(context)
        else:
            return Response(serializer.errors, 400)
