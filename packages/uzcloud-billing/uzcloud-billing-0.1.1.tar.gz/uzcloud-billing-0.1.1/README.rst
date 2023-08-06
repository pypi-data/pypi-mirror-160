====================
Uzcloud Billing
====================

Uzcloud Billing is a Django app to provide account with Uzcloud Billing account number. 


Quick start
-----------

1. Add "uzcloud_billing" to your INSTALLED_APPS ::

    INSTALLED_APPS = [
        ...
        'uzcloud_billing',
    ]

2. Include the uzcloud_billing urls in your project urls.py like this::

    path('api/billing', include('uzcloud_billing.urls')),

3. Add Following credentials to settings.py:
    | UZCLOUD_AUTH_URL = ""
    | UZCLOUD_BILLING_BASE_URL = ""
    | UZCLOUD_BILLING_CLIENT_ID = ""
    | UZCLOUD_BILLING_CLIENT_SECRET = ""

    | BILLING_SERVICE_WEBHOOK_USERNAME = ""
    | BILLING_SERVICE_WEBHOOK_PASSWORD = ""
    | BILLING_SERVICE_IDENT_RESPONSE_SERIALIZER = ""(default value is "billing.api.serializers.IdentResponseSerializer")

4. Run ``python manage.py migrate`` to create the uzcloud_billing models.
