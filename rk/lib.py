## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import urllib

from django.conf import settings

from rk.models import Transaction
from rk.defaults import RK_URL

__all__ = ["init"]

def init(data):
    """
    Init payment and redirect to robokassa site for checkout

    Required params:
    * amount - Amount to pay
    * [currency] - Suggested currency (can be changed by user)
    * [email] - User's email (can be changed by user)
    * [language] - "en" or "ru"
    """

    amount = data.get("amount", None)

    if amount is None:
        return None

    email = data.get("email", "")
    currency = data.get("currency", settings.RK_DEFAULT_CURRENCY)
    language = data.get("language", settings.RK_DEFAULT_LANGUAGE)

    login = settings.RK_MERCHANT_LOGIN
    pass1 = settings.RK_MERCHANT_PASS1
    description = settings.RK_DESCRIPTION_TPL % locals()

    # 2. Create transaction in DB
    tr = Transaction(amount=amount, description=description)
    tr.save()
    _id = tr.id

    signature = sign([login, amount, str(_id), pass1])

    # 3. Redirect to robokassa
    params = {"MrchLogin": login,
              "OutSum": amount,
              "InvId": _id,
              "Desc": description,
              "SignatureValue": signature,
              "IncCurrLabel": currency,
              "Email": email,
              "Culture": language}

    url = RK_URL + "?%s" % urllib.urlencode(params)

    return url

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sign(params):
    """
    Sign params
    """

    import hashlib

    return hashlib.md5(":".join(params)).hexdigest()
