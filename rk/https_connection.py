## coding=utf-8
##
## Max E. Kuzecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import httplib
import socket
import ssl
import urllib2

from lib import conf

def build_opener():
    """
    Build HTTPS connection opener

    From http://atlee.ca/blog/posts/blog20110210verifying-https-python.html
    """

    class VerifiedHTTPSConnection(httplib.HTTPSConnection):
        def connect(self):
            sock = socket.create_connection((self.host, self.port),
                                            self.timeout)
            if self._tunnel_host:
                self.sock = sock
                self._tunnel()

            # wrap the socket using verification with the root
            #    certs in trusted_root_certs
            self.sock = ssl.wrap_socket(sock,
                                        self.key_file,
                                        self.cert_file,
                                        cert_reqs=ssl.CERT_REQUIRED,
                                        ca_certs=conf("RK_SSL_CA_CERT_PATH"))

    # wraps https connections with ssl certificate verification
    class VerifiedHTTPSHandler(urllib2.HTTPSHandler):
        def https_open(self, req):
            return self.do_open(VerifiedHTTPSConnection, req)

    return urllib2.build_opener(VerifiedHTTPSHandler())
