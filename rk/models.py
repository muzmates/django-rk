## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.db import models

class Transaction(models.Model):
    """
    Payment transactions
    """

    amount = models.DecimalField(max_digits=15, decimal_places=2,
                                 help_text="Payment amount")

    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="Creation date")

    date_paid = models.DateTimeField(help_text="Payment date",
                                     default=None,
                                     null=True)

    description = models.TextField(max_length=100,
                                   help_text="Arbitrary payment notes")

    completed = models.BooleanField(default=False)

    currency = models.CharField(max_length=20,
                                default=None,
                                blank=True,
                                null=True)

    def __unicode__(self):
        return u"RK Transaction: %d %s" % (self.id, self.amount)
