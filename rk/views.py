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
import signals

log = logging.getLogger(__name__)

def init(req):
    """
    Init payment and redirect to robokassa site for checkout
    Required params can be passed using etiher GET or POST
    """

    data = req.POST

    # 2. Create transaction and redirect URL
    try:
        url = lib.init(data)

        signals.on_init.send_robust(sender=__name__, post=data)

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

    if lib.conf("RK_RESULT_URL_METHOD") == "GET":
        raw = req.GET
    else:
        raw = req.POST

    try:
        data = lib.verify(raw)
    except Exception as e:
        return err(*e.args)
    else:
        amount = Decimal(data["amount"])
        inv_id = data["inv_id"]

    # Check transaction
    try:
        tr = Transaction.objects.get(pk=inv_id)

        if tr.amount != amount:
            return err("Transaction amount mismatch: "\
                       "our=%s, their=%s", (tr.amount, amount))

        if tr.completed:
            return err("Transaction already completed: %s", inv_id)

        # Else everything is fine
        tr.completed = True
        tr.date_paid = now()
        tr.save()

        log.info("Transaction %s paid", inv_id)

        signals.on_transaction_created.send_robust(sender=__name__,
                                                   transaction=tr)

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

    if lib.conf("RK_RESULT_URL_METHOD") == "GET":
        raw = req.GET
    else:
        raw = req.POST

    try:
        data = lib.verify(raw)
    except Exception as e:
        return err(*e.args)
    else:
        inv_id = data["inv_id"]

    # Check transaction
    try:
        tr = Transaction.objects.get(pk=inv_id)

        if tr.amount != amount:
            return err("Transaction amount mismatch: "\
                       "our=%s, their=%s", tr.amount, amount)

        if not tr.completed:
            log.error("Transaction is not completed on success step: %s",
                      inv_id)
            tr.completed = True
            tr.date_paid = now()
            tr.save()

        signals.on_success.send_robust(sender=__name__, transaction=tr)

        return HttpResponse("")
    except Transaction.DoesNotExist:
        return err("Transaction with id=%s not found", inv_id)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def fail(req):
    """
    Payment failed
    """

    if lib.conf("RK_RESULT_URL_METHOD") == "GET":
        raw = req.GET
    else:
        raw = req.POST

    amount = raw.get("OutSum", "")
    inv_id = raw.get("InvId", "")

    signals.on_success.send_robust(sender=__name__, amount=amount,
                                   inv_id=inv_id)

    return HttpResponse("")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def err(msg=None, *params):
    if msg is not None:
        log.error(msg, *params)

        signals.on_transaction_failed.send_robust(sender=__name__,
                                                  error_msg=msg % *params)

    return HttpResponse("ERROR")
