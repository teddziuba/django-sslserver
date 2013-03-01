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

Start a SSL-enabled debug server:

  $ python manage.py runsslserver

The `runsslserver` command has the same syntax as `runserver`, except that it will
let you specify the server certificate and key.

`django-sslserver` is "batteries included", it comes with a self-signed certificate
and key, so you can start using it right away without mucking around with the `openssl`
command.
