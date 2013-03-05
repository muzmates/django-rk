## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from decimal import Decimal
import logging

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now

from rk import lib
from models import Transaction

log = logging.getLogger(__name__)

def init(req):
    """
    Init payment and redirect to robokassa site for checkout
    Required params can be passed using etiher GET or POST
    """

    # 1. Try to get required params
    if req.method == "POST":
        data = req.POST
    elif req.method == "GET":
        data = req.GET
    else:
        log.error("Invalid HTTP method: %s. GET or POST expected", req.method)

        return HttpResponseNotAllowed(["GET", "POST"])

    # 2. Create transaction and get redirect URL
    try:
        url = lib.init(data)

        return redirect(url)
    except Exception as e:
        log.error("Error in init: %s", e)

        return HttpResponseBadRequest()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def result(req):
    """
    Robokassa notification callback

    Following params are passed:
    * OutSum
    * InvId
    * SignatureValue
    """

    data = req.GET if settings.RK_RESULT_URL_METHOD == "GET" else req.POST

    amount = data.get("OutSum", None)
    inv_id = data.get("InvId", None)
    sig = data.get("SignatureValue", None)

    if None in (amount, inv_id, sig):
        return err("Required parameter not set: %s",
                  "OutSum" if amount is None else
                  ("InvId" if inv_id is None else "SignatureValue"))
    else:
        amount = Decimal(amount)

    # Else verify signature
    pass2 = settings.RK_MERCHANT_PASS2

    our_sig = lib.sign([str(amount), inv_id, pass2])

    if our_sig.lower() != sig.lower():
        return err("Signature mismatch: %s", sig)

    # Check transaction
    try:
        tr = Transaction.objects.get(pk=inv_id)

        if tr.amount != amount:
            return err("Transaction amount mismatch: "\
                       "our=%s, their=%s", tr.amount, amount)

        if tr.completed:
            return err("Transaction already completed: %s", inv_id)

        # Else everything is fine
        tr.completed = True
        tr.date_paid = now()
        tr.save()

        log.info("Transaction %s paid", inv_id)

        return HttpResponse("OK%s" % inv_id)
    except Transaction.DoesNotExist:
        return err("Transaction with id=%s not found", inv_id)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def success(req):
    """
    Payment succeeded

    Following params are passed:
    * OutSum
    * InvId
    * SignatureValue
    * Culture
    """

    data = req.GET if settings.RK_SUCCESS_URL_METHOD == "GET" else req.POST

    amount = data.get("OutSum", None)
    inv_id = data.get("InvId", None)
    sig = data.get("SignatureValue", None)

    if None in (amount, inv_id, sig):
        return err("Required parameter not set: %s",
                  "OutSum" if amount is None else
                  ("InvId" if inv_id is None else "SignatureValue"))

    # Else verify signature
    pass2 = settings.RK_MERCHANT_PASS2
    our_sig = lib.sign([amount, inv_id, pass2])

    if our_sig != sig:
        return err("Signature mismatch: %s != %s", sig, our_sig)

    # Check transaction
    try:
        tr = Transaction.objects.get(pk=inv_id)

        if tr.amount != amount:
            return err("Transaction amount mismatch: "\
                       "our=%s, their=%s", tr.amount, amount)

        return HttpResponse("OK%s" % inv_id)
    except Transaction.DoesNotExist:
        return err("Transaction with id=%s not found", inv_id)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def fail(req):
    """
    Payment failed
    """

    log.info("FAILED")

    return HttpResponse("failed")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def err(msg=None, *params):
    if msg is not None:
        log.error(msg, *params)

    return HttpResponse("ERROR")
