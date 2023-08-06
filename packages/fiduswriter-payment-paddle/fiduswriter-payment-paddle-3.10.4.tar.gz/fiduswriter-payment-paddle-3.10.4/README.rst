# fiduswriter-payment-paddle


Installation
------------

1. Sign up with Paddle.com, create plans and register a webhook (the URL is https:YOURWEBSITE.COM/api/payment/webhook/).

2. Add settings in configuration.py:

    > Under "INSTALLED_APPS" in configuration.py, add "payment"

    > PADDLE_VENDOR_ID = 547628

    > PADDLE_MONTHLY_PLAN_ID = 304958

    > PADDLE_SIX_MONTHS_PLAN_ID = 328473

    > PADDLE_ANNUAL_PLAN_ID = 232332

    > PADDLE_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
    > ...
    > -----END PUBLIC KEY-----'''

    > PADDLE_API_KEY = '234234a4b...36'


Additional steps if you don't use the Ubuntu Snap
-------------------------------------------------

1. Install `pycryptodome` and `phpserialize`:
    > pip install pycryptodome phpserialize

2. Run:

    > python manage.py migrate
