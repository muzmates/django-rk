## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import urllib

import lib

from models import Transaction

def init(amount, currency=None, email="", description="", language=None):
    """
    Init payment

    Params:
    * amount - Amount to pay
    * currency - Suggested currency (can be changed by user)
    * email - User's email (can be changed by user)
    * description - Transaction description
    * language - "en" or "ru"

    Return tuple (rk.models.Transaction instance, robokassa redirect URL)
    """

    if amount is None:
        return None

    currency = currency or lib.conf("RK_DEFAULT_CURRENCY")
    language = language or lib.conf("RK_DEFAULT_LANGUAGE")

    login = lib.conf("RK_MERCHANT_LOGIN")
    pass1 = lib.conf("RK_MERCHANT_PASS1")

    # 2. Create transaction in DB
    tr = Transaction(amount=amount, description=description)
    tr.save()
    _id = tr.id

    signature = lib.sign([login, amount, str(_id), pass1])

    # 3. Redirect to robokassa
    params = {"MrchLogin": login,
              "OutSum": amount,
              "InvId": _id,
              "Desc": description,
              "SignatureValue": signature,
              "IncCurrLabel": currency,
              "Email": email,
              "Culture": language}

    if lib.conf("RK_USE_TEST_SERVER"):
        rk_url = lib.conf("RK_TEST_URL")
    else:
        rk_url = lib.conf("RK_URL")

    url = rk_url + "?%s" % urllib.urlencode(params)

    return (tr, url)
