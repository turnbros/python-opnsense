.. Python-OPNsense documentation master file, created by
   sphinx-quickstart on Sat Mar 18 13:08:37 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Opnsense
========

Getting Started
~~~~~~~~~~~~~~~

First, install Python-OPNsense

.. code:: shell

    pip install python-opnsense

Next, create an instance of `Opnsense` by providing a path to a cert-bundle.

.. code:: python

    from opnsense_api import Opnsense
    opnsense = Opnsense(api_key="my_opnsense_api_key",
                        api_secret="my_opnsense_api_secret",
                        host="192.168.1.1",
                        ca_path="/path/to/opnsense/ca/cert_bundle.pem")

Another option is to create an instance using a base64 encoded CA certificate instead.

.. code:: python

    from opnsense_api import Opnsense
    opnsense = Opnsense(api_key="my_opnsense_api_key",
                        api_secret="my_opnsense_api_secret",
                        host="192.168.1.1",
                        ca_path="/path/to/opnsense/ca/cert_bundle.pem")

..  toctree::
    :hidden:
    :maxdepth: 1

    self

.. diagnostics:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Diagnostics

  diagnostics/*

.. firewall:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Firewall

  firewall/*

.. interfaces:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Interfaces

  interfaces/*

.. routing:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Routing

  routing/*

.. unbound:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Unbound

  unbound/*
