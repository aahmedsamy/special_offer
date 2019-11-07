from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.views import APIView
from datetime import timedelta

from helpers.permissions import IsPublisher, IsVerified, IsSearcher
from helpers.views import PaginatorView
from users.models import Publisher
from .models import (Offer, Discount, Category,
                     OfferFeature, Like, Story, StorySeen)
from .serializers import (OfferSerializer,
                          DiscountSerializer,
                          CategorySerializer, StorySeenSerializer, OfferFeatureSerializer, LikeOfferSerializer, LikeDiscountSerializer, StorySerializer, StorySerializerPost, PublisherStoriesSerializer)
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
        q = self.request.GET.get('q', None)
        queryset = Offer.objects.filter(status=Offer.PUBLISHED, start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(),).order_by('-id')
        if end_soon:
            end = timezone.now().today() + timedelta(days=3)
            queryset = queryset.filter(end_date__gte=end)
        if cat_id:
            queryset = queryset.filter(category_id=cat_id)
        if order_by == 'most_visited':
            queryset = queryset.order_by('-visited')
        if q:
            queryset = queryset.filter(name__contains=q)
        return queryset

    serializer_class = OfferSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', 'update', 'destroy',
                           'my', 'my_offers'
                           ]:
            permission_classes = [IsAuthenticated, IsPublisher, IsVerified]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    def partial_update(self, request, pk):
        offer = get_object_or_404(Offer.objects.filter(
            publisher=request.user.publisher), pk=pk)
        serializer = self.serializer_class(data=request.data, partial=True,
                                           context=self.get_serializer_context())
        if serializer.is_valid():
            offer = serializer.save()
            offer.status = Discount.PENDING
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
        end = timezone.now().today().date() + timedelta(days=3)

        queryset = self.get_queryset().filter(end_date__lte=end)

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
        return Response(context)

    @action(detail=False, methods=['get'])
    def my_offers(self, request):
        context = dict()
        filter_by = dict()
        page = request.GET.get('page', 1)
        status = str(request.GET.get('status', None))
        status_list = ['Pending', 'Declined', 'Published']
        if status not in status_list:
            context['error'] = "You should enter one of '{}' in 'status' query".format(
                status_list)
            return Response(context, status=400)
        filter_by['status'] = _(status)
        advertiser = request.user.publisher
        queryset = advertiser.publisher_offer.filter(start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(), **filter_by)
        context['count'] = queryset.count()
        queryset, cur_page, last_page = PaginatorView.queryset_paginator(
            queryset, page, 10)
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
        # for i in range(len(context['results'])):
        #     context['results'][i]['images'] = context['results'][i]['images'][0] if context['results'][i]['images'] else []
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
        q = self.request.GET.get("q", None)
        queryset = Discount.objects.filter(status=Discount.PUBLISHED, start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(),).order_by('-id')
        if end_soon:
            end = timezone.now().today() + timedelta(days=3)
            queryset = queryset.filter(end_date__lte=end)
        if cat_id:
            queryset = queryset.filter(category_id=cat_id)
        if order_by == 'most_visited':
            queryset = queryset.order_by('-visited')
        if q:
            queryset = queryset.filter(name__contains=q)
        return queryset

    serializer_class = DiscountSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', 'update', 'destroy',
                           'my',
                           ]:
            permission_classes = [IsAuthenticated, IsPublisher, IsVerified]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    def partial_update(self, request, pk):
        discount = get_object_or_404(Discount.objects.filter(
            publisher=request.user.publisher), pk=pk)
        serializer = DiscountSerializer(discount, data=request.data, partial=True,
                                        context=self.get_serializer_context())
        if serializer.is_valid():
            discount = serializer.save()
            discount.status = Discount.PENDING
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
        end = timezone.now().today().date() + timedelta(days=3)

        queryset = self.get_queryset().filter(end_date__lte=end)

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

        return Response(context)

    @action(detail=False, methods=['get'])
    def my_discounts(self, request):
        context = dict()
        filter_by = dict()
        page = request.GET.get('page', 1)
        status = str(request.GET.get('status', None))
        status_list = ['Pending', 'Declined', 'Published']
        if status not in status_list:
            context['error'] = "You should enter one of '{}' in 'status' query".format(
                status_list)
            return Response(context, status=400)
        filter_by['status'] = _(status)
        advertiser = request.user.publisher
        queryset = advertiser.publisher_discount.filter(start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(), **filter_by)
        context['count'] = queryset.count()
        queryset, cur_page, last_page = PaginatorView.queryset_paginator(
            queryset, page, 10)
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


class FeaturesViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):

    # queryset = Discount.objects.all()
    def get_queryset(self):
        if self.action in ['create', 'destroy', 'update']:
            advertiser = self.request.user.publisher
            queryset = OfferFeature.objects.filter(
                Q(offer__publisher=advertiser) | Q(discount__publisher=advertiser))
        elif self.action in ['retrieve']:
            queryset = OfferFeature.objects.all()
        return queryset

    serializer_class = OfferFeatureSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', 'destroy', 'update']:
            permission_classes = [IsAuthenticated, IsPublisher, IsVerified]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request):
        context = dict()
        advertiser = request.user.publisher
        error = False
        offer = request.data.get('offer', None)
        discount = request.data.get('discount', None)
        features = request.data.get('features', None)
        field_name = ""
        if discount and offer:
            context['detail'] = "It is not allowed to provide offer and discount at the same time"
            error = True

        elif not discount and not offer:
            context['detail'] = "Please provide offer or discount"
            error = True

        elif not features:
            context['features'] = "field is required and not empty."
            error = True
        if error:
            return Response(context, 400)
        if offer:
            field_name = "offer"
            ad_id = offer
            get_object_or_404(Offer.objects.filter(
                publisher=advertiser), id=ad_id)
        elif discount:
            field_name = "discount"
            ad_id = discount
            get_object_or_404(Discount.objects.filter(
                publisher=advertiser), id=ad_id)

        for i in range(len(features)):
            features[i][field_name] = ad_id

        serializer = OfferFeatureSerializer(
            data=features, many=True, context=self.get_serializer_context())

        if serializer.is_valid():
            serializer.save()
            context['detail'] = "Features Created successfully"
            return Response(context, 201)
        else:
            return Response(serializer.errors, 400)


class LikeViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    def get_queryset(self):
        searcher = self.request.user.searcher
        return Like.objects.filter(searcher=searcher)

    serializer_class = LikeOfferSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', 'remove',
                           ]:
            permission_classes = [IsAuthenticated, IsSearcher, IsVerified]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request):
        ad_type = request.GET.get("ad_type", None)
        ad_type_list = ['offer', 'discount']
        request.data['searcher'] = request.user.searcher.id
        context = dict()
        if ad_type in ad_type_list:
            if not request.data.get(ad_type, None):
                context['detail'] = "'{}' key is required".format(ad_type)
                return Response(context, 400)
            try:
                Like.objects.get(**request.data)
                context['detail'] = "You liked this ad before"
                return Response(context, 400)
            except Like.DoesNotExist:
                if ad_type == "offer":
                    serialser = LikeOfferSerializer(
                        data=request.data, context=self.get_serializer_context())
                elif ad_type == "discount":
                    serialser = LikeDiscountSerializer(
                        data=request.data, context=self.get_serializer_context())

                if serialser.is_valid():
                    serialser.save()
                    return Response(serialser.data)
                else:
                    return Response(serialser.errors, 400)

        else:
            context['detail'] = "query string must contain 'ad_type' with one of {} values".format(
                ad_type_list)
            return Response(context, 400)

    @action(detail=False, methods=['post'])
    def unlike(self, request):
        ad_type = request.GET.get("ad_type", None)
        ad_type_list = ['offer', 'discount']
        context = dict()
        if ad_type in ad_type_list:
            if not request.data.get(ad_type, None):
                context['detail'] = "'{}' key is required".format(ad_type)
                return Response(context, 400)
            if ad_type == "offer":
                offer = request.data.get("offer", None)
                like = self.get_queryset().filter(offer=offer)
            elif ad_type == "discount":
                discount = request.data.get("discount", None)
                like = self.get_queryset().filter(discount=discount)
            if like.exists():
                like.delete()
                context['detail'] = "Like removed successfully."
                return Response(context, 200)
            else:
                context['detail'] = "You don't like this ad"
                return Response(context, 400)

        else:
            context['detail'] = "query string mush contain 'ad_type' with one of {} values".format(
                ad_type_list)
            return Response(context, 400)


class PublisherStoryAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Publisher.objects.all().order_by(
        '-advertiser_stories__start_date').distinct()
    serializer_class = PublisherStoriesSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        filtered = Publisher.objects.filter(advertiser_stories__status=Story.APPROVED, advertiser_stories__start_time__lte=timezone.now(), advertiser_stories__end_time__gte=timezone.now()).order_by(
            'advertiser_stories__start_time').distinct()
        dist = []
        for i in filtered:
            if i not in dist:
                dist.append(i)
        return dist
        # return Publisher.objects.all()


class StorySeenAPI(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = StorySeen.objects.all()
    serializer_class = StorySeenSerializer
    permission_classes = [IsAuthenticated]


class StoryViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    # queryset = Offer.objects.all()
    def get_queryset(self,):
        queryset = Story.objects.filter(status=Story.APPROVED, start_time__lte=timezone.now(
        ), end_time__gte=timezone.now(),)
        return queryset

    serializer_class = StorySerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', 'partial_update', 'destroy', 'my_stories'
                           ]:
            permission_classes = [IsAuthenticated, IsPublisher, IsVerified]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    # def create(self, request):
    #     advertiser = request.user.publisher
    #     request.data['advertiser'] = advertiser.id
    #     serializer =  StorySerializerPost(data=request.data, context=self.get_serializer_context())
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def partial_update(self, request, pk):
    #     story = get_object_or_404(Story.objects.filter(
    #         advertiser=request.user.publisher), pk=pk)
    #     request.data['advertiser'] = advertiser.id
    #     serializer = StorySerializerPost(story, data=request.data, partial=True,
    #                                     context=self.get_serializer_context())
    #     serializer.is_valid(raise_exception=True)
    #     story = serializer.save()
    #     story.status = Story.PENDING
    #     story.save()
    #     return Response(serializer.data)

    def destroy(self, request, pk):
        context = dict()
        story = get_object_or_404(Story.objects.filter(
            advertiser=request.user.publisher), pk=pk)
        story.delete()
        context['detail'] = "Story deleted."
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def my_stories(self, request):
        context = dict()
        page = request.GET.get('page', 1)
        advertiser = request.user.publisher
        queryset = advertiser.advertiser_stories.all()
        context['count'] = queryset.count()
        queryset, cur_page, last_page = PaginatorView.queryset_paginator(
            queryset, page, 10)
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
        # for i in range(len(context['results'])):
        #     context['results'][i]['images'] = context['results'][i]['images'][0] if context['results'][i]['images'] else []
        return Response(context)
