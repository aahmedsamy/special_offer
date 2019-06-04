from django.shortcuts import get_object_or_404
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from datetime import timedelta

from helpers.permissions import IsPublisher, IsAuthenticatedAndVerified

from .models import Offer, Discount, Category
from .serializers import (OfferGetSerializer, OfferPostSerializer,
                          DiscountGetSerializer, DiscountPostSerializer,
                          CategorySerializer)
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
        order_by = self.request.GET.get('order_by', None)
        cat_id = self.request.GET.get('cat_id', None)
        end_soon = self.request.GET.get('end_soon', None)
        queryset = Offer.objects.filter(bending=False, start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(),).order_by('-id')
        if end_soon:
            end = timezone.now().today() + timedelta(days=3)
            queryset = queryset.filter(end_date__gte=end)
        if cat_id:
            queryset = queryset.filter(category_id=cat_id)
        if order_by == 'most_visited':
            queryset = queryset.order_by('-visited')
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
            return Response(serializer.errors, 400)

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

    def retrieve(self, request, pk):
        offer = get_object_or_404(self.get_queryset(), pk=pk)
        offer.visited = F('visited') + 1
        offer.save()
        offer = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(
            offer, context=self.get_serializer_context())
        return Response(serializer.data)

    def destroy(self, request, pk):
        context = dict()
        offer = get_object_or_404(
            self.get_queryset(), pk=pk, publisher=request.user.publisher)
        offer.delete()
        context['detail'] = "Offer deleted."
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def end_soon(self, request):
        context = dict()
        page = request.GET.get('page', 1)
        queryset = self.get_queryset()

        context['count'] = queryset.count()
        queryset, cur_page, last_page = PaginatorView.queryset_paginator(
            queryset, page, 3)
        context['previous'] = int(cur_page) - 1 if int(cur_page) > 1 else None
        context['next'] = cur_page + 1 \
            if int(cur_page) < last_page else None
        if context['previous']:
            context['previous'] = request.build_absolute_uri(
                "?page="+str(context['previous']))
        if context['next']:
            context['next'] = request.build_absolute_uri(
                "?page="+str(context['next']))
        context['results'] = self.serializer_class(
            queryset, many=True, context=self.get_serializer_context()).data
        context['results'] = self.sort_upon_points(context['results'])[:3]
        for i in range(len(context['results'])):
            context['results'][i]['images'] = context['results'][i]['images'][0] if context['results'][i]['images'] else []
        return Response(context)


class DiscountViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    # queryset = Offer.objects.all()
    def get_queryset(self,):
        order_by = self.request.GET.get('order_by', None)
        cat_id = self.request.GET.get('cat_id', None)
        end_soon = self.request.GET.get('end_soon', None)
        queryset = Discount.objects.filter(bending=False, start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(),).order_by('-id')
        if end_soon:
            end = timezone.now().today() + timedelta(days=3)
            queryset = queryset.filter(end_date__gte=end)
        if cat_id:
            queryset = queryset.filter(category_id=cat_id)
        if order_by == 'most_visited':
            queryset = queryset.order_by('-visited')
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
        serializer = DiscountPostSerializer(data=request.data,
                                            context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, 400)

    def partial_update(self, request, pk):
        context = dict()
        discount = get_object_or_404(
            publisher=request.user.publisher.id, pk=pk)
        del request.data['publisher']
        serializer = DiscountPostSerializer(discount, partial=True,
                                            context=self.get_serializer_context())
        if serializer.is_valid():
            discount = serializer.save()
            discount.bending = True
            discount.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, pk):
        discount = get_object_or_404(self.get_queryset(), pk=pk)
        discount.visited = F('visited') + 1
        discount.save()
        discount = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(
            discount, context=self.get_serializer_context())
        return Response(serializer.data)

    def destroy(self, request, pk):
        context = dict()
        discount = get_object_or_404(
            self.get_queryset(), pk=pk, publisher=request.user.publisher)
        discount.delete()
        context['detail'] = "Discount deleted."
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def end_soon(self, request):
        context = dict()
        page = request.GET.get('page', 1)
        queryset = self.get_queryset()

        context['count'] = queryset.count()
        queryset, cur_page, last_page = PaginatorView.queryset_paginator(
            queryset, page, 3)
        context['previous'] = int(cur_page) - 1 if int(cur_page) > 1 else None
        context['next'] = cur_page + 1 \
            if int(cur_page) < last_page else None
        if context['previous']:
            context['previous'] = request.build_absolute_uri(
                "?page="+str(context['previous']))
        if context['next']:
            context['next'] = request.build_absolute_uri(
                "?page="+str(context['next']))
        context['results'] = self.serializer_class(
            queryset, many=True, context=self.get_serializer_context()).data
        context['results'] = self.sort_upon_points(context['results'])[:3]
        for i in range(len(context['results'])):
            context['results'][i]['images'] = context['results'][i]['images'][0] if context['results'][i]['images'] else []
        return Response(context)


class CategoryViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    # queryset = Offer.objects.all()
    def get_queryset(self,):
        queryset = Category.objects.all()
        return queryset

    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}
