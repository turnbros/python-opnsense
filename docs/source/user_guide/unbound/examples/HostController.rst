.. code:: python

    from opnsense_api import Opnsense
    from opnsense_api.unbound.host_controller import HostOverride, UnboundResourceRecord

    opnsense = Opnsense(api_key="my_opnsense_api_key",
                        api_secret="my_opnsense_api_secret",
                        host="192.168.1.1",
                        ca_path="/path/to/opnsense/ca/cert_bundle.pem")

Creating Unbound host overrides
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    new_host_override = HostOverride(uuid=None,
                                     hostname="",
                                     domain="google.com",
                                     server="1.1.1.1",
                                     rr=UnboundResourceRecord.A,
                                     description="google-override")

    opnsense.unbound_dns.host_override_controller.add(new_host_override)
