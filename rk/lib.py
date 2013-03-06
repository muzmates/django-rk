## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import urllib

from django.conf import settings

from rk.models import Transaction
from rk import defaults

__all__ = ["conf",
           "init",
           "sign",
           "verify",
           "get_hook"
           ]

def conf(val):
    """
    Get configuration param
    """

    return getattr(settings, val, getattr(defaults, val))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    currency = data.get("currency", conf("RK_DEFAULT_CURRENCY"))
    language = data.get("language", conf("RK_DEFAULT_LANGUAGE"))

    login = conf("RK_MERCHANT_LOGIN")
    pass1 = conf("RK_MERCHANT_PASS1")
    description = conf("RK_DESCRIPTION_TPL") % locals()

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

    if conf("RK_USE_TEST_SERVER"):
        rk_url = conf("RK_TEST_URL")
    else:
        rk_url = conf("RK_URL")

    url = rk_url + "?%s" % urllib.urlencode(params)

    return url

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sign(params):
    """
    Sign params
    """

    import hashlib

    return hashlib.md5(":".join(params)).hexdigest()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def verify(data):
    """
    Verify incoming request from robokassa
    """

    amount = data.get("OutSum", None)
    inv_id = data.get("InvId", None)
    sig = data.get("SignatureValue", None)

    if None in (amount, inv_id, sig):
        raise Exception("Required parameter not set: %s",
                        "OutSum" if amount is None else \
                            ("InvId" if inv_id is None else "SignatureValue"))

    # Else verify signature
    pass2 = conf("RK_MERCHANT_PASS2")
    our_sig = sign([amount, inv_id, pass2])

    if our_sig.lower() != sig.lower():
        raise Exception("Signature mismatch: %s != %s", sig, our_sig)
    else:
        return {"amount": amount, "inv_id": inv_id}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_hook():
    """
    Get registered hook instance
    """

    hook_data = conf("RK_HOOK_CLASS").split(".")
    hook_package = ".".join(hook_data[:-1])
    hook_class = hook_data[-1]

    module = __import__(hook_package, globals(), locals(), [hook_class], -1)

    inst = getattr(module, hook_class)()

    if not isinstance(inst, RKBaseHook):
        raise Exception("Class %s doesn't extend RKBaseHook", hook_data)
    else:
        return inst
