from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from uzcloud_billing.models import BillingAccount


class PaymentEventSerializer(serializers.Serializer):
    AccountNumber = serializers.CharField(max_length=16, min_length=9)
    paymentType = serializers.CharField(max_length=20)
    Amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    Balance = serializers.DecimalField(max_digits=10, decimal_places=2)


class IdentSerializer(serializers.Serializer):
    AccountNumber = serializers.CharField(max_length=16, min_length=9)

    def validate_AccountNumber(self, value):
        client = User.objects.filter(billing_account__account_number=value)
        if not client.exists():
            raise NotFound(detail={"error_code": "account_number_not_exist"})
        return value

    def validate(self, attrs):
        self.billing_account = BillingAccount.objects.get(
            account_number=attrs["AccountNumber"]
        )
        return attrs


class IdentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
