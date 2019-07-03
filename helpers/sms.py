from django.conf import settings

from twilio.rest import Client


class Twilio:
    def __init__(self):
        self.account_sid = settings.ACCOUNT_SID
        self.auth_token = settings.AUTH_TOKEN

    @classmethod
    def send_message(cls, body, from_, to):
        obj = cls()
        client = Client(obj.account_sid, obj.auth_token)
        message = client.messages.create(
            from_=from_,
            body=body,
            to=to
        )
        return message
