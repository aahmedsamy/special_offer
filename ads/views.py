from django.utils import timezone

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny)

from .models import Ad
from .serializers import (AdSerializer,)


class AdViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        queryset = Ad.objects.filter(start_date__lte=timezone.now(
        ), end_date__gte=timezone.now(),)
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
