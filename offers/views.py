from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from datetime import datetime

from helpers.permissions import IsPublisher, IsAuthenticatedAndVerified

from .models import Offer, Discount, Category
from .serializers import OfferGetSerializer, OfferPostSerializer
# Create your views here.


class OfferViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    # queryset = Offer.objects.all()
    def get_queryset(self,):
        querystring = self.request.GET.dict()
        queryset = Offer.objects.filter(bending=False, start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(), **querystring)
        return queryset

    serializer_class = OfferGetSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', 'update', 'destroy',
                           'my',
                           ]:
            permission_classes = [IsPublisher, IsAuthenticatedAndVerified]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request):
        request.data['publisher'] = request.user.publisher.id
        serializer = OfferPostSerializer(data=request.data,
                                         context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def partial_update(self, request, pk):
        context = dict()
        offer = get_object_or_404(publisher=request.user.publisher.id, pk=pk)
        del request.data['publisher']
        serializer = OfferPostSerializer(offer, partial=True,
                                         context=self.get_serializer_context())
        if serializer.is_valid():
            offer = serializer.save()
            offer.bending = True
            offer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
