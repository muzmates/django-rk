## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

class RKException(Exception):
    """
    Base exception
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ResponseMissingData(RKException):
    """
    Some data fields are missing in API response

    Argument: field name missing
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ResponseDataMismatch(RKException):
    """
    Some data fields in reponse do not match with those in DB

    Argument: mismatching field name
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SignatureMismatch(RKException):
    """
    Signature mismatch

    Arguments: provided signature, generated signature
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TransactionIsCompleted(RKException):
    """
    Transaction is already completed

    Argument: Transaction instance
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TransactionNotFound(RKException):
    """
    Transaction with provided token cannot be found in the database

    Argument:
    """

    pass
