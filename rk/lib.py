## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.conf import settings

import defaults

def conf(val):
    """
    Get configuration param
    """

    return getattr(settings, val, getattr(defaults, val))

def sign(params):
    """
    Sign params
    """

    import hashlib

    return hashlib.md5(":".join(params)).hexdigest()

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

def get_merchant_url(method):
    """
    Get a merchant URL for specific method
    """

    return "%s/%s" % (conf("RK_MERCHANT_URL"), method)

def get_out_sum(amount2pay, currency):
    """
    Get amount to pay including the RK fee
    """

    import urllib
    import urllib2

    import xml.etree.ElementTree as ET
    from contextlib import closing
    from https_connection import build_opener

    def ns(tag):
        return "{%s}%s" % ("http://merchant.roboxchange.com/WebService/", tag)

    params = {
        "MerchantLogin": conf("RK_MERCHANT_LOGIN"),
        "IncCurrLabel": currency,
        "IncSum": amount2pay,
    }

    req = urllib2.Request("%s?%s" % (get_merchant_url("CalcOutSumm"),
                                     urllib.urlencode(params)))

    opener = build_opener()

    with closing(opener.open(req)) as stream:
        xml = stream.read()
        root = ET.fromstring(xml)
        code = root.find("%s/%s" % (ns("Result"), ns("Code"))).text

        if code != "0":
            raise Exception("Call failed: code=%s,xml=%s" % (str(code), str(xml)))

        return float(root.find("%s" % ns("OutSum")).text)
