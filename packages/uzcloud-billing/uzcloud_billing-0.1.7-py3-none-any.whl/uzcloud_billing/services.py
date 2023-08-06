def update_account_balance(*, billing_account, balance: float):
    billing_account.balance = balance
    billing_account.save()
