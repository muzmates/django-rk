## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.http import HttpResponse

import cur

RK_MERCHANT_LOGIN = "merchant login"
RK_MERCHANT_PASS1 = "password1"
RK_MERCHANT_PASS2 = "password2"
RK_DEFAULT_CURRENCY = cur.WMR
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
RK_SSL_CA_CERT_PATH = "/etc/ssl/certs/ca-certificates.crt"

## Robokassa URLs
RK_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"
RK_TEST_URL = "http://test.robokassa.ru/Index.aspx"
RK_MERCHANT_URL = "https://merchant.roboxchange.com/WebService/Service.asmx"
