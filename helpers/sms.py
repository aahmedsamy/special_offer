from django.conf import settings

    
# from twilio.rest import Client

class Nexmo:
    def __init__(self):
        import nexmo
        self.client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
    
    @classmethod
    def send_message(cls, from_, to, text):
        obj = cls()
        message = dict()
        context = dict()
        message['from'] = from_
        message['text'] = text
        message['to'] = to
        message['type'] = "unicode"
        response = obj.client.send_message(
            message
        )

        if response["messages"][0]["status"] == "0":
            context['status'] = "success"
            context['message'] = "Message sent successfully."
            return context 
        else:
            context['status'] = "fail"
            context['message'] = "Message failed with error: {}".format(response['messages'][0]['error-text'])
            return context
# class Twilio:
#     def __init__(self):
#         self.account_sid = settings.TWILIO_ACCOUNT_SID
#         self.auth_token = settings.TWILIO_AUTH_TOKEN
#         self.number = settings.TWILIO_NUMBER

#     @classmethod
#     def send_message(cls, body, from_, to):
#         obj = cls()
#         client = Client(obj.account_sid, obj.auth_token)
#         message = client.messages.create(
#             from_=from_,
#             body=body,
#             to=to
#         )
#         return message
