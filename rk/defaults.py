## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.http import HttpResponse

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
RK_ERROR_CALLBACK = lambda req, tr, err: HttpResponse()
RK_CANCEL_CALLBACK = lambda req, amount, order_id: HttpResponse()

## Robokassa URL
RK_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"
RK_TEST_URL = "http://test.robokassa.ru/Index.aspx"
