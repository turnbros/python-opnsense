.. code:: python

    from opnsense_api import Opnsense
    opnsense = Opnsense(api_key="my_opnsense_api_key",
                        api_secret="my_opnsense_api_secret",
                        host="192.168.1.1",
                        ca_path="/path/to/opnsense/ca/cert_bundle.pem")

Creating a VXLAN interface
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    opnsense()
