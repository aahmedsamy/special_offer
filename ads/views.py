from django.utils import timezone

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny)

from helpers.views import PaginatorView

from .models import Ad
from .serializers import (AdSerializer,)


class AdViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        queryset = Ad.objects.filter(start_date__lte=timezone.now(
        ), end_date__gte=timezone.now())
        return queryset

    serializer_class = AdSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['retrieve', 'list']:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        context = dict()
        position = request.GET.get('position', None)
        page = request.GET.get('page', 1)
        if not position or not position in ['Top', 'Buttom']:
            context['detail'] = "'position' quertystring key is required with value ('Top' or 'Buttom')."
            return Response(context, 400)

        queryset = self.get_queryset().filter(position=position)
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
