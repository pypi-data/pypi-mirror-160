from django.db import models
from django.contrib.auth.models import User

from uzcloud_billing.utils import generate_account_number


class BillingAccount(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="billing_account"
    )
    account_number = models.CharField(
        max_length=255, default=generate_account_number, unique=True
    )

    def __str__(self):
        return f"{self.user} - {self.account_number}"
