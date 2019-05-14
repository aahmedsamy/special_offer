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

from .models import User, Searcher, Publisher
from .serializers import (UserSerializer,
                          SearcherSerializer,
                          PublisherSerializer,
                          PasswordResetingSerializer,
                          PasswordChangeSerializer,
                          SignupSerializer,
                          LoginSerializer,
                          VerficationSerializer)
from helpers.numbers import gen_rand_number
from helpers.permissions import IsAuthenticatedAndVerified
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
        elif self.action in ['my']:
            permission_classes = [IsAuthenticatedAndVerified]
        elif self.action in ['change_password', 'edit']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

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
                basic_serializer = SignupSerializer(data=basic_info)
                if basic_serializer.is_valid():
                    basic_info = basic_serializer.data.copy()
                    del basic_info['password1']
                    if user_type == 'searcher':
                        more_serializer = SearcherSerializer(data=more_info)
                    else:
                        more_serializer = PublisherSerializer(data=more_info)

                    if more_serializer.is_valid():
                        basic = User.objects.create_user(**basic_info)
                        more = more_serializer.save()
                        if user_type == 'searcher':
                            basic.searcher = more
                        else:
                            basic.publisher = more
                        basic.save()
                        context['basic_info'] = UserSerializer(basic).data
                        context['basic_info']['publisher']['image'] = request.build_absolute_uri(
                            context['basic_info']['publisher']['image'])
                        context['basic_info']['publisher']['trading_doc'] = request.build_absolute_uri(
                            context['basic_info']['publisher']['trading_doc'])
                        # context['more_info'] = more_serializer.data
                        logging.info("{} - New user {}".format(
                            api_code, basic.email,
                        ))
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
        serializer = PasswordChangeSerializer(data=request.data)
        user = request.user
        context = dict()
        if serializer.is_valid():
            cur_password = user.password
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
                return Response(context, status=status.HTTP_205_RESET_CONTENT)
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
        serializer = LoginSerializer(data=request.data)
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
            return Response(context, status=status.HTTP_200_OK)
        else:
            logging.warning('{} - faild login {}'.format(
                api_code, serializer.errors
            ))
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def send_pass_reset_code(self, request,):
        api_code = self.__class__.__name__, "send_pass_reset_code"
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
        api_code = self.__class__.__name__, "send_email_verification_code"
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
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        api_code = self.__class__.__name__, "reset_password"
        serializer = PasswordResetingSerializer(data=request.data)
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
                return Response(context, status=status.HTTP_205_RESET_CONTENT)
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
        serializer = VerficationSerializer(data=request.data)
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
                return Response(context, status=status.HTTP_205_RESET_CONTENT)
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
        context = dict()
        user_type = ""
        try:
            user = Searcher.objects.get(searcher=request.user)
            user_type = "searcher"
        except Searcher.DoesNotExist:
            try:
                user = Publisher.objects.get(publisher=request.user)
                user_type = "publisher"
            except Publisher.DoesNotExist:
                return Response("Unhandled exception, please contact adminstrator", 400)

        if user_type == "searcher":
            serializer = SearcherSerializer(
                user, data=request.data, partial=True)
        elif user_type == "publisher":
            serializer = PublisherSerializer(
                user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logging.info('{} - {} data updated successfully'.format(
                api_code, request.user.email
            ))
            context['detail'] = "User Data updated successfully"
            return Response(context, status=status.HTTP_200_OK)
        else:
            logging.warning('{} - {} updating data user: {}, error{}'.format(
                api_code, request.user.email, serializer.errors
            ))
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
