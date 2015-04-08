=================
Django SSL Server
=================

Django SSL Server is a SSL-enabled development server for the Django Framework.

Getting Started
===============

Install the module in your Python distribution or virtualenv::

  $ pip install django-sslserver

Add the application to your `INSTALLED_APPS`::

  INSTALLED_APPS = (...
  "sslserver",
  ...
  )

Start a SSL-enabled debug server::

  $ python manage.py runsslserver [--addrport 127.0.0.1:9000]


You'll now be able to access your Django app on https://localhost:8000/


Browser Certificate Errors
==========================

Using the default settings, your local browser will make all sorts of noise that it *doesn't trust the certificate*. **This is expected.**

Django SSL Server ships "batteries included" with a self-signed server certificate. With self-signed certificates,
the server is effectively telling the user, "I'm such-and-such server, because I said so". Whereas, with a commercial
SSL certificate, the server tells the user, "I'm Bank of America, because VeriSign said so (or any other commercial certificate authority)."

**Using self-signed certificates for development is fine, but not for production**. In production, your users will see
the same ugly certificate warning you're seeing now. That's bad.

There are two options for making the certificate warning go away in development:

**Option 1**: Tell your browser to explicitly trust the certificate. You can do this in your browser's "advanced settings"
tab, by installing ``sslserver/certs/development.crt`` as a trusted certificate. The mechanism for this varies from browser to browser.

**Option 2**: Use a commercial SSL certificate. If you have a certificate/key pair from a commercial certificate authority,
you can tell Django SSL Server to use it with the following arguments::

  $ python manage.py runsslserver --certificate /path/to/certificate.crt --key /path/to/key.key


Third-Party Static File Handlers
================================

If you're using a wrapper around your WSGI application such as dj_static or WhiteNoise, you probably want to let it handle serving
static files. Otherwise, you may see 404s when requesting static files. You can disable the default behavior by using the ``--nostatic``
option.

Getting Involved
================

Feel free to open pull requests or issues. GitHub is the canonical location of this project.
