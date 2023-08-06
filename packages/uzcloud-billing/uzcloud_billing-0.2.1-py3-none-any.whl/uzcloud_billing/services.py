import uzcloud_billing.utils as utils
from uzcloud_billing.signals import payment_completed_signal


def update_account_balance(*, billing_account, balance: float):
    billing_account.balance = balance
    billing_account.save()


def make_invoice(account_number: str, amount: float, reason: str, data: dict):
    response = utils.uzcloud_service.make_invoice(
        account_number=account_number, amount=amount, reason=reason
    )
    payment_completed_signal.send(sender=None, data=data)
    return response
