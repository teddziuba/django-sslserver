#!/usr/bin/env python
from setuptools import setup, find_packages
import sslserver

setup(name="django-sslserver",
      version=sslserver.__version__,
      author="Ted Dziuba",
      author_email="tjdziuba@gmail.com",
      description="An SSL-enabled development server for Django",
      url="https://github.com/teddziuba/django-sslserver",
      packages=find_packages(exclude=['demo']),
      include_package_data=True,
      install_requires=["Django >= 1.8"],
      license="MIT",
      classifiers=[
          "Environment :: Web Environment",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Framework :: Django",
          "Framework :: Django :: 1.8",
          "Framework :: Django :: 1.9",
          "Framework :: Django :: 1.10",
          "Framework :: Django :: 1.11"],
      )
