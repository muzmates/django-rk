# Overview

django-rk is a django application for integrating payment system
robokassa.ru.

# Module settings

```python
RK_MERCHANT_LOGIN = "merchant login"
RK_MERCHANT_PASS1 = "password1"
RK_MERCHANT_PASS2 = "password2"
RK_DEFAULT_CURRENCY = "WMZ"
RK_DEFAULT_LANGUAGE = "en"
RK_RESULT_URL_METHOD = "GET"
RK_SUCCESS_URL_METHOD = "GET"
RK_CANCEL_URL_METHOD = "GET"
RK_USE_TEST_SERVER = True
RK_RESULT_SUCCESS_CALLBACK = lambda req, tr: None
RK_RESULT_ERROR_CALLBACK = lambda req, tr, err: None
RK_SUCCESS_CALLBACK = lambda req, tr: HttpResponse()
RK_ERROR_CALLBACK = lambda req, tr, err: None
RK_CANCEL_CALLBACK = lambda req, amount, order_id: HttpResponse()
```

# Settings on robokassa site:

Result URL: http://yourserver/rk/result
Success URL: http://yourserver/rk/success
Cancel URL: http://yourserver/rk/cancel

# Installation

1. Add `rk` application to your `INSTALLED_APPS`

2. Add following to your main urls.py:

```python
    url('rk/', include('rk.urls')),
```

3. Run manage.py syncdb && manage.py migrate rk

