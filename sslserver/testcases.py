import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.testcases import LiveServerTestCase, LiveServerThread, QuietWSGIRequestHandler

from sslserver.management.commands.runsslserver import (
    SecureHTTPServer, WSGIRequestHandler, default_ssl_files_dir,
)


class SecureQuietWSGIRequestHandler(WSGIRequestHandler, QuietWSGIRequestHandler):
    pass


class SecureLiveServerThread(LiveServerThread):
    def _create_server(self):
        cert_file = os.path.join(default_ssl_files_dir(), "development.crt")
        key_file = os.path.join(default_ssl_files_dir(), "development.key")

        return SecureHTTPServer(
            (self.host, self.port),
            SecureQuietWSGIRequestHandler,
            cert_file,
            key_file,
        )


class SecureLiveServerTestCase(LiveServerTestCase):
    server_thread_class = SecureLiveServerThread


class SecureStaticLiveServerTestCase(StaticLiveServerTestCase):
    server_thread_class = SecureLiveServerThread
