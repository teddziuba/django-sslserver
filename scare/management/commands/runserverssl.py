from optparse import make_option
import ssl


from django.core.servers.basehttp import WSGIRequestHandler
from django.core.servers.basehttp import WSGIServer
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.servers.basehttp import get_internal_wsgi_application


class SecureHTTPServer(WSGIServer):
    def __init__(self, address, handler_cls, certificate, key):
        super(SecureHTTPServer, self).__init__(address, handler_cls)
        self.socket = ssl.wrap_socket(self.socket, certfile=certificate,
                                      keyfile=key, server_side=True)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--certificate",  default="/foo/bar",
                    help="Path to the certificate"),
        make_option("--key", default="/foo/bar/baz",
                    help="Path to the key file")
    )

    help = "Run a Django development server over HTTPS"

    def get_handler(self):
        return get_internal_wsgi_application()

    def handle(self, *args, **options):
        self.key_file = options.get("key")
        self.certificate_file = options.get("certificate")
        server = SecureHTTPServer(("0.0.0.0", 8000), WSGIRequestHandler,
                                  self.certificate_file, self.key_file)
        server.set_app(self.get_handler())
        server.serve_forever()
