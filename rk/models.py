## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Transaction(models.Model):
    """
    Payment transactions
    """

    amount = models.DecimalField(max_digits=15, decimal_places=2,
                                 help_text=_("Payment amount"))

    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text=_("Creation date"))

    date_paid = models.DateTimeField(help_text=_("Payment date"),
                                     default=None,
                                     null=True)

    description = models.TextField(max_length=100,
                                   help_text=_("Arbitrary payment notes"))

    completed = models.BooleanField(default=False)
