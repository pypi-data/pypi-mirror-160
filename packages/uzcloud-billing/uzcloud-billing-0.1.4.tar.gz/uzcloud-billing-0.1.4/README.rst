====================
Uzcloud Billing
====================

Uzcloud Billing is a Django app to provide account with Uzcloud Billing account number. 


Quick start
-----------

1.Add "rest_framework" and "uzcloud_billing" to your INSTALLED_APPS :

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'uzcloud_billing',
    ]

2.Include the uzcloud_billing urls in your project urls.py like this :

.. code-block:: python

    path('api/billing/', include('uzcloud_billing.urls')),

3.Add Following credentials to settings.py :

.. code-block:: python

    UZCLOUD_AUTH_URL = ""
    UZCLOUD_BILLING_BASE_URL = ""
    UZCLOUD_BILLING_CLIENT_ID = ""
    UZCLOUD_BILLING_CLIENT_SECRET = ""

    BILLING_SERVICE_WEBHOOK_USERNAME = ""
    BILLING_SERVICE_WEBHOOK_PASSWORD = ""
    BILLING_SERVICE_IDENT_RESPONSE_SERIALIZER = ""(Note that this serializer must get **User object** as instance)

4.Run ``python manage.py migrate`` to create the uzcloud_billing models.
