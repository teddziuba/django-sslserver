from datetime import datetime
from optparse import make_option
from distutils.version import LooseVersion
import os
import ssl
import sys

from django.core.servers.basehttp import WSGIRequestHandler
from django.core.servers.basehttp import WSGIServer
from django.core.management.base import CommandError
from django.core.management.commands import runserver
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.utils.importlib import import_module
from django import get_version

try:
    from django.core.servers.basehttp import WSGIServerException
except ImportError:
    from socket import error as WSGIServerException

if LooseVersion(get_version()) >= LooseVersion('1.5'):
    from django.utils._os import upath
else:
    upath = unicode

class SecureHTTPServer(WSGIServer):
    def __init__(self, address, handler_cls, certificate, key):
        super(SecureHTTPServer, self).__init__(address, handler_cls)
        self.socket = ssl.wrap_socket(self.socket, certfile=certificate,
                                      keyfile=key, server_side=True,
                                      ssl_version=ssl.PROTOCOL_TLSv1,
                                      cert_reqs=ssl.CERT_NONE)


class WSGIRequestHandler(WSGIRequestHandler):
    def get_environ(self):
        env = super(WSGIRequestHandler, self).get_environ()
        env['HTTPS'] = 'on'
        return env


def default_ssl_files_dir():
    app_module = import_module("sslserver")
    mod_path = os.path.dirname(upath(app_module.__file__))
    ssl_dir = os.path.join(mod_path, "certs")
    return ssl_dir


class Command(runserver.Command):
    option_list = runserver.Command.option_list + (
        make_option("--certificate",
                    default=os.path.join(default_ssl_files_dir(),
                                         "development.crt"),
                    help="Path to the certificate"),
        make_option("--key",
                    default=os.path.join(default_ssl_files_dir(),
                                         "development.key"),
                    help="Path to the key file")
    )

    help = "Run a Django development server over HTTPS"

    def get_handler(self, *args, **options):
        """
        Returns the static files serving handler wrapping the default handler,
        if static files should be served. Otherwise just returns the default
        handler.

        """
        handler = super(Command, self).get_handler(*args, **options)
        use_static_handler = options.get('use_static_handler', True)
        insecure_serving = options.get('insecure_serving', False)
        if use_static_handler:
            return StaticFilesHandler(handler)
        return handler

    def check_certs(self, key_file, cert_file):
        # TODO: maybe validate these? wrap_socket doesn't...

        if not os.path.exists(key_file):
            raise CommandError("Can't find key at %s" % key_file)
        if not os.path.exists(cert_file):
            raise CommandError("Can't find certificate at %s" %
                               cert_file)


    def inner_run(self, *args, **options):
        # Django did a shitty job abstracting this.

        key_file = options.get("key")
        cert_file = options.get("certificate")
        self.check_certs(key_file, cert_file)

        from django.conf import settings
        from django.utils import translation

        threading = options.get('use_threading')
        shutdown_message = options.get('shutdown_message', '')
        quit_command = (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C'

        self.stdout.write("Validating models...\n\n")
        self.validate(display_num_errors=True)
        self.stdout.write((
            "%(started_at)s\n"
            "Django version %(version)s, using settings %(settings)r\n"
            "Starting development server at https://%(addr)s:%(port)s/\n"
            "Using SSL certificate: %(cert)s\n"
            "Using SSL key: %(key)s\n"
            "Quit the server with %(quit_command)s.\n"
        ) % {
            "started_at": datetime.now().strftime('%B %d, %Y - %X'),
            "version": self.get_version(),
            "settings": settings.SETTINGS_MODULE,
            "addr": self._raw_ipv6 and '[%s]' % self.addr or self.addr,
            "port": self.port,
            "quit_command": quit_command,
            "cert": cert_file,
            "key": key_file
        })
        # django.core.management.base forces the locale to en-us. We should
        # set it up correctly for the first request (particularly important
        # in the "--noreload" case).
        translation.activate(settings.LANGUAGE_CODE)

        try:
            handler = self.get_handler(*args, **options)
            server = SecureHTTPServer((self.addr, int(self.port)),
                                      WSGIRequestHandler,
                                      cert_file, key_file)
            server.set_app(handler)
            server.serve_forever()

        except WSGIServerException:
            e = sys.exc_info()[1]
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS = {
                13: "You don't have permission to access that port.",
                98: "That port is already in use.",
                99: "That IP address can't be assigned-to.",
            }
            try:
                error_text = ERRORS[e.args[0].args[0]]
            except (AttributeError, KeyError):
                error_text = str(e)
            self.stderr.write("Error: %s" % error_text)
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)

