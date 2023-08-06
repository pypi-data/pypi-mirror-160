from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework.views import APIView
from rest_framework.response import Response

from uzcloud_billing.models import BillingAccount
from uzcloud_billing.services import update_account_balance
from uzcloud_billing.signals import balance_filled_signal
from .serializers import PaymentEventSerializer, IdentSerializer
from .permissions import PaymentEventBasicAuthentication


class BalanceFilledEventView(APIView):
    authentication_classes = [PaymentEventBasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = PaymentEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        balance_filled_signal.send(
            sender=BillingAccount, data=serializer.validated_data
        )
        update_account_balance(
            billing_account=serializer.billing_account,
            balance=serializer.validated_data["Balance"],
        )
        return Response()


class IdentEventView(APIView):
    authentication_classes = [PaymentEventBasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = IdentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_serializer = import_string(
            settings.UZCLOUD_BILLING["IDENT_RESPONSE_SERIALIZER"]
        )
        return Response(
            response_serializer(instance=serializer.billing_account.user).data
        )
