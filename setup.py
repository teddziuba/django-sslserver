from distutils.core import setup

setup(name="django-sslserver",
      version="0.1",
      author="Ted Dziuba",
      author_email="tjdziuba@gmail.com",
      description="An SSL-enabled development server for Django",
      url="https://github.com/teddziuba/django-sslserver",
      packages=["sslserver",
                "sslserver.management",
                "sslserver.management.commands"],
      package_dir={"sslserver": "sslserver"},
      package_data={"sslserver": ["certs/development.crt",
                                  "certs/development.key",
                                  "certs/server.csr"]},
      install_requires=["setuptools",
                        "Django >= 1.4"],
      )
