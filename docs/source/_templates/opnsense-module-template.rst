{{ objname | escape | underline}}

.. automodule:: {{ fullname }}

{% block classes %}
{% if classes %}

Classes
~~~~~~~

.. autosummary::
  :toctree:
  :template: custom-class-template.rst
{% for item in classes %}
  {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block modules %}
{% if modules %}

Modules
~~~~~~~

.. autosummary::
   :toctree:
   :template: custom-module-template.rst
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

Getting Started
~~~~~~~~~~~~~~~

.. include:: ../examples/getting-started.rst
