## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import urllib

from django.conf import settings

import defaults

from models import Transaction

__all__ = ["conf",
           "sign",
           "verify",
           ]

def conf(val):
    """
    Get configuration param
    """

    return getattr(settings, val, getattr(defaults, val))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sign(params):
    """
    Sign params
    """

    import hashlib

    return hashlib.md5(":".join(params)).hexdigest()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def verify(data, password):
    """
    Verify incoming request from robokassa
    """

    import ex

    amount = data.get("OutSum", None)
    inv_id = data.get("InvId", None)
    sig = data.get("SignatureValue", None)

    if amount is None:
        raise ex.ResponseMissingData("OutSum")
    elif inv_id is None:
        raise ex.ResponseMissingData("InvId")
    elif sig is None:
        raise ex.ResponseMissingData("SignatureValue")

    # Else verify signature
    our_sig = sign([amount, inv_id, password])

    if our_sig.lower() != sig.lower():
        raise ex.SignatureMismatch(sig, our_sig)
    else:
        return {"amount": amount, "inv_id": inv_id}
