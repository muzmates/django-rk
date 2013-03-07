# Overview

django-rk is a django application for integrating payment system
robokassa.ru.

# Module settings

```python
RK_MERCHANT_LOGIN = "merchant login"
RK_MERCHANT_PASS1 = "password1"
RK_MERCHANT_PASS2 = "password2"
RK_DESCRIPTION_TPL = "muzmates.com payment"
RK_DEFAULT_CURRENCY = "WMZ"
RK_DEFAULT_LANGUAGE = "en"
RK_RESULT_URL_METHOD = "GET"
RK_SUCCESS_URL_METHOD = "GET"
RK_FAIL_URL_METHOD = "GET"
RK_SUCCESS_URL = "success case redirect"
RK_FAIL_URL = "failure redirect"
RK_USE_TEST_SERVER = True
```

# Settings on robokassa site:

Result URL: http://yourserver/{RK_URL_PREFIX}/result
Success URL: http://yourserver/{RK_URL_PREFIX}/success
Fail URL: http://yourserver/{RK_URL_PREFIX}/fail

# Installation

1. Add `rk` application to your `INSTALLED_APPS`

2. Add following to your main urls.py:

```python
    url('rk/', include('rk.urls')),
```

3. Run manage.py syncdb && manage.py migrate rk

# Signals

There are several signals defined in the module rk.signals, which can be used
to get notified on different events in transaction processing flow.

To connect to one of these signal, use:

```python
from rk.signals import on_success

on_success.connect(callback, dispatch_uid="my_id")
```
