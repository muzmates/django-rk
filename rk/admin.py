## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.contrib import admin

from models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date_created", "date_paid", "amount", "completed"]

admin.site.register(Transaction, TransactionAdmin)
