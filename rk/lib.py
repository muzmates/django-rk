## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.conf import settings

import defaults

__all__ = ["conf",
           "sign",
           "verify",
           "get_merchant_url",
           "get_currencies",
           ]

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

def get_currencies(language="en"):
    """
    Get available currencies

    Returns list of group dicts:

    [{"code": string(),
      "description": string(),
      "data": {"label": string(), "name": string()}}]
    """

    import urllib
    import urllib2
    import xml.etree.ElementTree as ET

    from contextlib import closing
    from https_connection import build_opener

    ns = lambda tag: "{%s}%s" % ("http://merchant.roboxchange.com/WebService/", tag)

    params = {
        "MerchantLogin": conf("RK_MERCHANT_LOGIN"),
        "Language": language
    }

    req = urllib2.Request(get_merchant_url("GetCurrencies"),
                          urllib.urlencode(params))

    opener = build_opener()

    with closing(opener.open(req)) as stream:
        result = []

        xml = stream.read()
        root = ET.fromstring(xml)
        code = root.find("%s/%s" % (ns("Result"), ns("Code"))).text

        if code != "0":
            raise Exception("Call failed: code=%s,xml=%s" % str(code), str(xml))

        for group in root.findall("%s/%s" % (ns("Groups"), ns("Group"))):
            gr = {"code": group.attrib.get("Code", None),
                  "description": group.attrib.get("Description", None),
                  "data": {}
                  }

            items = group.find(ns("Items"))

            for currency in items.findall(ns("Currency")):
                gr["data"]["label"] = currency.get("Label", None)
                gr["data"]["name"] = currency.get("Name", None)

            result.append(gr)

        return result

