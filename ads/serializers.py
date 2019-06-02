from django.utils import timezone

from rest_framework import serializers

from users.serializers import PublisherSerializer

from .models import Ad


class AdSerializer(serializers.ModelSerializer):

      class Meta:
         model = Ad
         exclude = ('start_date', 'end_date')
