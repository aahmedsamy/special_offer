from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from .models import User, Searcher, Publisher, SearcherNotification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'searcher', 'publisher')
        depth = 1


class SearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Searcher
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    trading_doc = Base64ImageField()

    class Meta:
        model = Publisher
        fields = "__all__"


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=265)
    password1 = serializers.CharField(max_length=265)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'searcher', 'publisher', 'password', 'password1')

    def validate(self, data):
        """
        Validate if password and password1 are identical.
        """
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                "'password' and 'password1' fields aren't the same!")
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password1 = serializers.CharField(max_length=20)

    def validate(self, data):
        """
        Validate if password and password1 are identical.
        """
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                "'password' and 'password1' fields aren't the same!")
        return data


class PasswordResetingSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    pass_reset_code = serializers.CharField(max_length=7)
    password = serializers.CharField(max_length=255)
    password1 = serializers.CharField(max_length=20)

    def validate(self, data):
        """
        Validate if password and password1 are identical.
        """
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                "'password' and 'password1' fields aren't the same!")
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=20)


class VerficationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class NotificationSerializer(serializers.ModelSerializer):
    offer = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = SearcherNotification
        exclude = ['searcher']
    
    def get_offer(self, obj):
        ret = dict()
        if obj.offer:
            ret['offer'] = obj.offer.name
            ret['category'] = obj.offer.category.name
            return ret
    
    def get_discount(self, obj):
        ret = dict()
        if obj.discount:
            ret['discount'] = obj.discount.name
            ret['category'] = obj.discount.category.name
            return ret
