from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail


from rest_framework import (viewsets, mixins, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework_jwt.settings import api_settings

from datetime import datetime

from .models import User
from .serializers import (UserSerializer,
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
        serializer = SignupSerializer(data=request.data)
        api_code = self.__class__.__name__, "sign_up"
        if serializer.is_valid():
            del request.data['password1']
            user_type = request.data.get('user_type', None)
            phone = request.data.get('phone', None)
            if not user_type:
                return Response({'detail': 'user_type field is required.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if int(user_type) == User.PREMUIM and not phone:
                return Response({'detail': 'phone field is required for '
                                 'premium users.'},
                                status=status.HTTP_400_BAD_REQUEST)
            request.data['email'] = request.data['email'].lower().strip()
            user = User.objects.create_user(**request.data)
            user.verification_code = gen_rand_number(6)
            user.save()
            subject = 'Special offer verification code'
            message = str(user.verification_code)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            logging.info("{} - New user {}".format(
                api_code, user.email,
            ))
            return Response({'detail': 'User created Successfully.'},
                            status=status.HTTP_201_CREATED)
        else:
            logging.warning("{} - user creationg failed {}".format(
                api_code, serializer.errors,
            ))
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

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
        user = request.user
        serializer = UserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logging.info('{} - {} data updated successfully'.format(
                api_code, request.user.email
            ))
            context['detail'] = _("User Data updated successfully")
            return Response(context, status=status.HTTP_200_OK)
        else:
            logging.warning('{} - {} updating data user: {}, error{}'.format(
                api_code, request.user.email, serializer.errors
            ))
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my(self, request,):
        api_code = self.__class__.__name__, "my"
        context = dict()
        user = request.user
        queryset = user.property_user.all()
        page = request.GET.get("page", 1)

        if queryset:
            queryset, cur_page, last_page = PaginatorView.queryset_paginator(
                queryset, page, 10)
            serializer = PropertyListSerializer(queryset, many=True)
            context['previous'] = cur_page - 1 if int(cur_page) > 1 else None
            context['next'] = cur_page + 1 \
                if int(cur_page) < last_page else None
            context['count'] = last_page
            context['detail'] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = "No property yet!"
            return Response(context, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        api_code = self.__class__.__name__, "properties"
        context = dict()
        user = get_object_or_404(self.queryset, id=pk)
        queryset = Property.objects.filter(
            publisher_id=user.id, visible=True, bending=False)
        page = request.GET.get("page", 1)
        if queryset:
            queryset, cur_page, last_page = PaginatorView.queryset_paginator(
                queryset, page, 10)
            serializer = PropertyListSerializer(queryset, many=True)
            context['previous'] = cur_page - 1 if int(cur_page) > 1 else None
            context['next'] = cur_page + 1 \
                if int(cur_page) < last_page else None
            context['count'] = last_page
            context['detail'] = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['detail'] = _("No property yet!")
            return Response(context, status=status.HTTP_204_NO_CONTENT)