FilterRule
==========

.. currentmodule:: opnsense_api.firewall.filter_controller

.. autoclass:: FilterRule
   :members:
   :show-inheritance:
   :inherited-members:


.. automethod:: __init__



Methods
~~~~~~~

.. autosummary::

  ~FilterRule.__init__
  ~FilterRule.action_valid
  ~FilterRule.construct
  ~FilterRule.copy
  ~FilterRule.dict
  ~FilterRule.direction_valid
  ~FilterRule.from_orm
  ~FilterRule.ipprotocol_valid
  ~FilterRule.json
  ~FilterRule.parse_file
  ~FilterRule.parse_obj
  ~FilterRule.parse_raw
  ~FilterRule.ports_only_defined_when_tcp_or_udp
  ~FilterRule.schema
  ~FilterRule.schema_json
  ~FilterRule.update_forward_refs
  ~FilterRule.validate






Attributes
~~~~~~~~~~

.. autosummary::

  ~FilterRule.enabled
  ~FilterRule.sequence
  ~FilterRule.description
  ~FilterRule.action
  ~FilterRule.quick
  ~FilterRule.interface
  ~FilterRule.direction
  ~FilterRule.ipprotocol
  ~FilterRule.protocol
  ~FilterRule.source_net
  ~FilterRule.source_not
  ~FilterRule.source_port
  ~FilterRule.destination_net
  ~FilterRule.destination_not
  ~FilterRule.destination_port
  ~FilterRule.gateway
  ~FilterRule.log
  ~FilterRule.uuid



Examples
~~~~~~~~

.. include:: ../examples/FilterRule.rst