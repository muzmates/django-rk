## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.dispatch import Signal

# Called before sending init request to robokassa
#
# Arguments: POST dict
on_init = Signal(providing_args=["post"])

# Called when robokassa server calls result URL and
# transaction is saved to database
#
# Arguments: rk.models.Transaction instance
on_transaction_created = Signal(providing_args=["transaction"])

# Called when transaction cannot be created due to some error
#
# Arguments: error string
on_transaction_error = Signal(providing_args=["error_msg"])

# Called when robokassa server calls success URL
#
# Arguments: rk.models.Transaction instance
on_success = Signal(providing_args=["transaction"])

# Called when robokassa server calls fail URL
#
# Arguments: amount and order id
on_fail = Signal(providing_args=["amount", "inv_id"])
