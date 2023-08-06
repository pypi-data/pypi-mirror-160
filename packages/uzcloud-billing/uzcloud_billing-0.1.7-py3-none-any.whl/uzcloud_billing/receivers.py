from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from uzcloud_billing.models import BillingAccount

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_billing_account(sender: User, instance: User, created, **kwargs):
    if created:
        BillingAccount.objects.create(user=instance)
