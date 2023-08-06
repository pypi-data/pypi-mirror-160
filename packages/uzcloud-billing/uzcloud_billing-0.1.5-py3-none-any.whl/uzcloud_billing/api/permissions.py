import base64
from django.conf import settings

from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions


class PaymentEventBasicAuthentication(BasicAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if not auth_header:
            raise exceptions.AuthenticationFailed("Please provice basic authentication")
        encoded_credentials = auth_header.split(" ")[
            1
        ]  # Removes "Basic " to isolate credentials
        decoded_credentials = (
            base64.b64decode(encoded_credentials).decode("utf-8").split(":")
        )
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        if (
            username != settings.UZCLOUD_BILLING["WEBHOOK_USERNAME"]
            or password != settings.UZCLOUD_BILLING["WEBHOOK_PASSWORD"]
        ):
            raise exceptions.AuthenticationFailed("Invalid username or password")
        return (True, True)
