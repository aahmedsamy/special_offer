from rest_framework_jwt.settings import api_settings

from users.models import User
from calendar import timegm

from datetime import datetime


def jwt_payload_handler(user):
    name = user.get_full_name()
    payload = {
        'user_id': user.pk,
        'email': user.email,
        'name': name,
    }

    issued_at = datetime.utcnow()
    expires_at = issued_at + api_settings.JWT_EXPIRATION_DELTA

    payload['iat'] = timegm(issued_at.utctimetuple())
    payload['exp'] = timegm(expires_at.utctimetuple())

    return payload


def jwt_get_username_from_payload(payload):
    return payload.get("email")


def jwt_response_payload_handler(token, user=None, request=None):
    if user.user_type == User.PREMUIM and user.verified:
        return{
            'token': token,
        }
    return {
        'token': token,
    }
