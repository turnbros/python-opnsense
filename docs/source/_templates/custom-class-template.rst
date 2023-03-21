{{ objname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :show-inheritance:
   :inherited-members:

{% block methods %}
.. automethod:: __init__

{% if methods %}

Methods
~~~~~~~

.. autosummary::
{% for item in methods %}
  ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block attributes %}
{% if attributes %}

Attributes
~~~~~~~~~~

.. autosummary::
{% for item in attributes %}
  ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

Examples
~~~~~~~~

.. include:: ../examples/{{ name }}.rst
