:html_theme.sidebar_secondary.remove:

Connecting to an OPNsense Firewall
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the devices CA certificate in hand, create an instance of `Opnsense` by providing a path to the cert-bundle.

..  code:: python

    from opnsense_api import Opnsense
    opnsense = Opnsense(api_key="my_opnsense_api_key",
                        api_secret="my_opnsense_api_secret",
                        host="192.168.1.1",
                        ca_path="/path/to/opnsense/ca/cert_bundle.pem")

Another option is to create an instance using a base64 encoded CA certificate instead.

..  code:: python

    from opnsense_api import Opnsense
    opnsense = Opnsense(api_key="my_opnsense_api_key",
                        api_secret="my_opnsense_api_secret",
                        host="192.168.1.1",
                        ca_path="/path/to/opnsense/ca/cert_bundle.pem")
