## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from decimal import Decimal

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from rk import lib, ex
from models import Transaction

def return_err():
    return HttpResponse("ERROR")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def result(req):
    """
    Robokassa notification callback

    Following params are passed:
    * OutSum
    * InvId
    * SignatureValue
    """

    successf = lib.conf("RK_RESULT_SUCCESS_CALLBACK")
    failuref = lib.conf("RK_RESULT_ERROR_CALLBACK")
    tr = None

    if lib.conf("RK_RESULT_URL_METHOD") == "GET":
        raw = req.GET
    else:
        raw = req.POST

    try:
        data = lib.verify(raw, lib.conf("RK_MERCHANT_PASS2"))
    except Exception as e:
        return failuref(req, tr, e)

    amount = Decimal(data["amount"])
    inv_id = data["inv_id"]

    # Check transaction
    try:
        tr = Transaction.objects.get(pk=inv_id)

        if tr.amount != amount:
            raise ex.ResponseDataMismatch("amount")

        if tr.completed:
            raise ex.TransactionIsCompleted(tr)

        # Else everything is fine
        tr.completed = True
        tr.date_paid = now()
        tr.save()

        successf(req, tr)

        return HttpResponse("OK%s" % inv_id)
    except Transaction.DoesNotExist:
        failuref(req, tr, ex.TransactionNotFound())

        return return_err()
    except Exception as e:
        failuref(req, tr, e)

        return return_err()

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

    successf = lib.conf("RK_SUCCESS_CALLBACK")
    failuref = lib.conf("RK_ERROR_CALLBACK")
    tr = None

    if lib.conf("RK_RESULT_URL_METHOD") == "GET":
        raw = req.GET
    else:
        raw = req.POST

    try:
        data = lib.verify(raw, lib.conf("RK_MERCHANT_PASS1"))
    except Exception as e:
        return failuref(req, tr, e)

    # Check transaction
    try:
        inv_id = data.get("inv_id", None)
        amount = Decimal(data["amount"])

        tr = Transaction.objects.get(pk=inv_id)

        if tr.amount != amount:
            raise ex.ResponseDataMismatch("amount")

        if tr.completed:
            tr.completed = True
            tr.date_paid = now()
            tr.save()

        return successf(req, tr)
    except Transaction.DoesNotExist:
        return failuref(req, tr, ex.TransactionNotFound())
    except Exception as e:
        return failuref(req, tr, e)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def cancel(req):
    """
    Payment canceled
    """

    cancelf = lib.conf("RK_CANCEL_CALLBACK")

    if lib.conf("RK_CANCEL_URL_METHOD") == "GET":
        raw = req.GET
    else:
        raw = req.POST

    amount = raw.get("OutSum", "")
    inv_id = raw.get("InvId", "")

    return cancelf(req, amount, inv_id)
