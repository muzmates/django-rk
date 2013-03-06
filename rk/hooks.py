## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

class RKBaseHook(object):
    def on_init(self, post):
        """
        Called before sending init request to robokassa

        Arguments: POST dict
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def on_result(self, transaction):
        """
        Called when robokassa server calls result URL and
        transaction is saved to database

        Arguments: rk.models.Transaction instance
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def on_success(self, transaction):
        """
        Called when robokassa server calls success URL

        Arguments: rk.models.Transaction instance
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def on_fail(self, amount, inv_id):
        """
        Called when robokassa server calls fail URL

        Arguments: amount and order id
        """

        pass
