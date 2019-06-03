from django.shortcuts import get_object_or_404
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny)
from datetime import timedelta

from helpers.permissions import IsPublisher, IsAuthenticatedAndVerified

from paymentgateway import (generate_client_token, transact, find_transaction)
from .models import Transaction, TransactionAttempt
from .serializers import CheckoutSerializer
# from .serializers import (OfferGetSerializer, OfferPostSerializer,
#                           DiscountGetSerializer, DiscountPostSerializer)
# Create your views here.


class TransactionViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self,):
        queryset = TransactionAttempt.objects.filter(
            advertiser=self.request.user.publisher
        )
        return queryset


    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['create', 'update', 'list', 'retrieve', 'client_token']:
            permission_classes = [IsPublisher, IsAuthenticatedAndVerified]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}

    @action(detail=False, methods=['get'])
    def client_token(self, request):
        context = dict()
        context['client_token'] = generate_client_token()
        return Response(context)

    @action(detail=False, methods=['post'])
    def create_checkout():
        context = dict()
        payment = dict()
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            result = transact({
                'amount': serializer['amount'],
                'payment_method_nonce': serializer['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                context['clue'] =
                payment['advertiser'] = request.user.publisher
                payment['payment_id'] = result.transaction.id
                payment['amount'] = result.transaction.amount
                payment['status'] = TransactionAttempt.PAID
                TransactionAttempt.objects.create(**payment)
                context['clue'] = result.transaction.id
                return Response(context)
            else:
                for x in result.errors.deep_errors:
                    context['Error'][x.code] = x.message
                return Response(context, 400)
