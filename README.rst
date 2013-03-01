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

  $ python manage.py runsslserver


You'll now be able to access your Django app on https://localhost:8000/


Browser Certificate Errors
==========================

Using the default settings, your local browser will make all sorts of noise that it *doesn't trust the certificate*. *This is expected.*

Django SSL Server ships "batteries included" with a self-signed server certificate. With self-signed certificates,
the server is effectively telling the user, "I'm such-and-such server, because I said so". Whereas, with a commercial
SSL certificate, the server tells the user, "I'm Bank of America, because VeriSign said so (or any other commercial certificate authority)."

**Using self-signed certificates for development is fine, but not for production**. In production, your users will see
the same ugly certificate warning you're seeing now. That's bad.

