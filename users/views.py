from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail


from rest_framework import (viewsets, mixins, status)
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework_jwt.settings import api_settings

from datetime import datetime

from offers.models import Category, Offer, FollowedCategory
from offers.serializers import CategorySerializer

from helpers.sms import Twilio

from .models import User, Searcher, Publisher, SearcherNotification, AdvertiserNotification
from .serializers import (UserSerializer,
                          SearcherSerializer,
                          PublisherSerializer,
                          PasswordResetingSerializer,
                          PasswordChangeSerializer,
                          SignupSerializer,
                          LoginSerializer,
                          VerficationSerializer,
                          SearcherNotificationSerializer,
                          AdvertiserNotificationSerializer)
from helpers.numbers import gen_rand_number
from helpers.permissions import (IsPublisher, IsVerified, IsSearcher)
from helpers.views import PaginatorView


import logging


def generate_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class UserViewSet(
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_class = (FileUploadParser,)
    

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['retrieve', 'sign_up', 'login',
                           'send_pass_reset_code', 'reset_password', 'verify',
                           ]:
            permission_classes = [AllowAny]
        elif self.action in ['advertiser_insights']:
            permission_classes = [IsAuthenticated, IsPublisher, IsVerified]
        elif self.action in ['send_phone_verification_code', 'verify_phone']:
            permission_classes = [IsAuthenticated, IsPublisher]
        elif self.action in ['followed_categories', 'follow_category']:
            permission_classes = [IsSearcher, IsVerified]
        elif self.action in ['change_password', 'edit', 'my_data']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=False, methods=['post'])
    def sign_up(self, request,):
        api_code = self.__class__.__name__, "sign_up"
        context = dict()
        user_type_values = ['searcher', 'publisher']
        user_type = request.GET.get('user_type', None)
        if user_type:
            if user_type in user_type_values:
                basic_info = request.data.get('basic_info', None)
                more_info = request.data.get('more_info', None)
                if not basic_info or not more_info:
                    context['detail'] = []
                    if not basic_info:
                        context['detail'].append(
                            "'basic_info' key is required.")
                    if not more_info:
                        context['detail'].append(
                            "'more_info' key is required.")
                    context['sample'] = {
                        "basic_info": {
                            "email": "s.specialoffer@gmail.com",
                            "password": "23498ods",
                            "password1": "23498ods",
                        },
                        "more_info": {
                            "name": "sh",
                        }
                    }
                    return Response(context, 400)
                basic_serializer = SignupSerializer(data=basic_info, context=self.get_serializer_context())
                if basic_serializer.is_valid():
                    basic_info = basic_serializer.data.copy()
                    del basic_info['password1']
                    if user_type == 'searcher':
                        more_serializer = SearcherSerializer(data=more_info, context=self.get_serializer_context())
                    else:
                        more_serializer = PublisherSerializer(data=more_info, context=self.get_serializer_context())

                    if more_serializer.is_valid():
                        basic = User.objects.create_user(**basic_info)
                        more = more_serializer.save()
                        if user_type == 'searcher':
                            basic.searcher = more
                        else:
                            basic.publisher = more
                        basic.save()
                        # context['basic_info'] = UserSerializer(basic).data
                        # if user_type == "publisher":
                        #     context['basic_info']['publisher']['image'] = request.build_absolute_uri(
                        #         context['basic_info']['publisher']['image'])
                        #     context['basic_info']['publisher']['trading_doc'] = request.build_absolute_uri(
                        #         context['basic_info']['publisher']['trading_doc'])
                        # context['more_info'] = more_serializer.data
                        logging.info("{} - New user {}".format(
                            api_code, basic.email,
                        ))
                        context['message'] = "User created successfully."
                        token = generate_token(basic)
                        context['Token'] = token
                        context['user_id'] = basic.id
                        context['user_type'] = "advertiser" if basic.is_publisher() else "searcher"
                        if context['user_type'] == "searcher":
                            context['liked_ads'] = basic.searcher.get_liked_ads()
                        return Response(context, 201)
                    else:
                        return Response(more_serializer.errors, 400)
                else:
                    return Response(basic_serializer.errors, 400)
            else:
                context['detail'] = "Expected {} values for '{}' query string key!".format(
                    user_type_values, "user_type"
                )
                return Response(context, 400)
        else:
            context['detail'] = "'user_type' query string is required!"
            return Response(context, 400)

    @action(detail=False, methods=['post'])
    def change_password(self, request,):
        api_code = self.__class__.__name__, "change_password"
        serializer = PasswordChangeSerializer(data=request.data, context=self.get_serializer_context())
        user = request.user
        context = dict()
        if serializer.is_valid():
            if user.check_password(serializer.data['old_password']):
                user.set_password(serializer.data['password'])
                user.save()
                logging.info("{} - password changed for user {}.".format(
                    api_code, user.email,
                ))
                send_mail(
                    _("Change special offer password"),
                    _("You special offer password has been changed."),
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                context['detail'] = _("Password changed successfully.")
                return Response(context, status=200)
            else:
                logging.warning("{} - old password is wrong, user {}.".format(
                    api_code, user.email,
                ))
                context['detail'] = _("Old password is wrong!")
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            logging.warning("{} - user : {} ERROR {}".format(
                api_code, user.email, serializer.errors
            ))
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request,):
        api_code = self.__class__.__name__, "login"
        serializer = LoginSerializer(data=request.data, context=self.get_serializer_context())
        context = dict()
        if serializer.is_valid():
            user = auth.authenticate(
                email=request.data['email'], password=request.data['password'])
            if user is None:
                context['detail'] = _("Unable to login with provided \
                     credentials")
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            token = generate_token(user)
            context['Token'] = token
            context['verified'] = user.is_verified()
            context['user_id'] = user.id
            context['user_type'] = "advertiser" if user.is_publisher() else "searcher"
            if context['user_type'] == "searcher":
                context['liked_ads'] = user.searcher.get_liked_ads()
            return Response(context, status=status.HTTP_200_OK)
        else:
            logging.warning('{} - faild login {}'.format(
                api_code, serializer.errors
            ))
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def send_pass_reset_code(self, request,):
        email = request.GET.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email.strip())
                user.pass_reset_code = gen_rand_number(7)
                user.save()
                send_mail(
                    'Reset special offer password',
                    'Reset password code "{}"'.format(user.pass_reset_code),
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                return Response({"detail": "reset password code sent to {}".format(
                    user.email)})
            except User.DoesNotExist:
                return Response({"detail": "Email doesn't exist"},
                                status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"details": "Please provide 'email' query string"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(detail=False, methods=['get'])
    def send_email_verification_code(self, request,):
        email = request.GET.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email.strip())
                user.verification_code = gen_rand_number(6)
                user.save()
                send_mail(
                    'SPO Email verification code',
                    'code "{}"'.format(user.verification_code),
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                return Response({"detail": "Email verification code sent to {}".format(
                    user.email)})
            except User.DoesNotExist:
                return Response({"detail": "Email doesn't exist"},
                                status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"details": "Please provide 'email' query string"},
                            status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def send_phone_verification_code(self, request,):
        advertiser = request.user.publisher
        advertiser.phone_verification_code = gen_rand_number(6)
        advertiser.save()
        body = 'SPO Phone verification code "{}"'.format(advertiser.phone_verification_code),
        to = advertiser.phone
        Twilio.send_message(
            body = body,
            to = to
        )
        return Response({"detail": "Phone verification code sent to {}".format(
            advertiser.phone)})
    
    @action(detail=False, methods=['post'])
    def verify_phone(self, request):
        serializer = VerficationSerializer(data=request.data, context=self.get_serializer_context())
        context = dict()
        if serializer.is_valid():
            advertiser = request.user.publisher
            if advertiser.phone_verification_code == serializer.data['code']:
                advertiser.phone_verification_code = None
                advertiser.phone_verified = True
                advertiser.save()
                context['detail'] = _("Your account verified successfuly")
                return Response(context, status=200)
            else:
                context['detail'] = _("Wrong verification code!")
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        api_code = self.__class__.__name__, "reset_password"
        serializer = PasswordResetingSerializer(data=request.data, context=self.get_serializer_context())
        context = dict()
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    email=serializer.data['email'],
                    pass_reset_code=serializer.data['pass_reset_code'])
                user.set_password(serializer.data['password'])
                user.save()
                send_mail(
                    'special offer password',
                    'password reseted successfully at "{}"'.format(
                        datetime.now()),
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                logging.info('{} - Password resetted successfully with email {}'.format(
                    api_code, user.email
                ))
                context['detail'] = _("Password Resetted successfully")
                return Response(context, status=200)
            except User.DoesNotExist:
                logging.warning('{} - Invalid code with email {}'.format(
                    api_code, serializer.data['email']
                ))
                context['detail'] = _("invalid code!")
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            logging.warning("{} - email: {}, errors: {}".format(
                api_code, request.data['email'], serializer.errors
            ))
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        api_code = self.__class__.__name__, "verify"
        serializer = VerficationSerializer(data=request.data, context=self.get_serializer_context())
        context = dict()
        if serializer.is_valid():
            email = request.data.get('email', None)
            try:
                user = User.objects.get(
                    email=email)
                if user.is_verified():
                    logging.info('{} - User {} is verified'.format(
                        api_code, user.email
                    ))
                    context['detail'] = _("Invalid URL!")
                    return Response(context, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                logging.warning("{} - Invalid verification url with email: {}".format(
                    api_code, email
                ))
                context['detail'] = _("Invalid URL!")
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            if user.verification_code == serializer.data['code']:
                user.verification_code = None
                user.verified = True
                user.save()
                logging.info("{} - user {} verfied".format(
                    api_code, user.email
                ))
                context['detail'] = _("Your account verified successfuly")
                return Response(context, status=200)
            else:
                logging.warning('{} - wrong verification code for {}'.format(
                    api_code, user.email
                ))
                context['detail'] = _("Wrong verification code!")
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def edit(self, request, pk=None):
        api_code = self.__class__.__name__, "edit"
        required_keys = ['basic', 'more']
        context = dict()
        for key in required_keys:
            if key not in request.data.keys():
                context['detail'] = "{} are required keys.".format(
                    required_keys)
                return Response(context, 400)

        basic = request.data['basic']
        more = request.data['more']
        user = request.user
        if request.user.is_publisher():
            b_serializer = UserSerializer(user, data=basic, partial=True, context=self.get_serializer_context())
            publisher = Publisher.objects.get(publisher__id=user.id)
            m_serialser = PublisherSerializer(
                publisher, data=more, partial=True, context=self.get_serializer_context())
        elif request.user.is_searcher():
            b_serializer = UserSerializer(user, data=basic, partial=True, context=self.get_serializer_context())
            searcher = Searcher.objects.get(searcher__id=user.id)
            m_serialser = SearcherSerializer(
                searcher, data=more, partial=True, context=self.get_serializer_context())

        if b_serializer.is_valid():
            if m_serialser.is_valid():
                m_serialser.save()
                b_serializer.save()
                user = User.objects.get(id=user.id)
                context['detail'] = UserSerializer(user, context=self.get_serializer_context()).data
                return Response(context, 200)
            else:
                context['more'] = m_serialser.errors
                return Response(context, 400)
        else:
            context['basic'] = b_serializer.errors
            return Response(context, 400)

    @action(detail=False, methods=['get'])
    def advertiser_insights(self, request):
        advertiser = request.user.publisher
        context = dict()
        context['likes'] = advertiser.likes()
        context['total_visites'] = advertiser.total_visits()
        context['active_posts'] = advertiser.active_posts_cnt()
        return Response(context, 200)

    @action(detail=False, methods=['get'])
    def followed_categories(self, request):
        searcher = request.user.searcher
        queryset = Category.objects.filter(
            followed_category_category__searcher=searcher)
        serializer = CategorySerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def follow_category(self, request):
        cat_id = request.data.get('cat_id', None)
        searcher = request.user.searcher
        context = dict()
        if cat_id:
            cat = get_object_or_404(Category.objects.all(), id=cat_id)
            FollowedCategory.objects.get_or_create(
                searcher=searcher,
                category=cat
            )
            context['detail'] = "the requested category added to your followed categories."
            return Response(context, 201)
        else:
            context['detail'] = "'cat_id' key is required"
            return Response(context, 400)

    @action(detail=False, methods=['post'])
    def unfollow_category(self, request):
        cat_id = request.data.get('cat_id', None)
        searcher = request.user.searcher
        context = dict()
        if cat_id:
            cat = get_object_or_404(Category.objects.all(), id=cat_id)
            follow = get_object_or_404(
                FollowedCategory.objects.all(), category=cat, searcher=searcher)
            follow.delete()
            context['detail'] = "the requested category removed from your followed categories."
            return Response(context, 200)
        else:
            context['detail'] = "'cat_id' key is required"
            return Response(context, 400)
    
    @action(detail=False, methods=['get'])
    def my_data(self, request):
        serializer = self.serializer_class(request.user, context=self.get_serializer_context())
        return Response(serializer.data)

class SearcherNotificationViewSet(
    mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        searcher = self.request.user.searcher
        return SearcherNotification.objects.filter(searcher=searcher)

    serializer_class = SearcherNotificationSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['list',
                           ]:
            permission_classes = [IsAuthenticated, IsSearcher, IsVerified]
        return [permission() for permission in permission_classes]

class AdvertiserNotificationViewSet(
    mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        advertiser = self.request.user.publisher
        return AdvertiserNotification.objects.filter(advertiser=advertiser)

    serializer_class = AdvertiserNotificationSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['list',
                           ]:
            permission_classes = [IsAuthenticated, IsPublisher, IsVerified]
        return [permission() for permission in permission_classes]