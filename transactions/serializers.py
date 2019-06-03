from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):

    amount = serializers.FloatField(min_value=0.0)
    payment_method_nonce = serializers.CharField()
    clue = serializers.IntegerField(min_value=1)
