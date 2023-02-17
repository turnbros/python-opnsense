# python-opnsense
A Python library for the Opnsense API

## Getting Started

### Supported Controllers and Services
- Firewall Aliases
- Firewall Filter Rules
- Unbound Domain Overrides
- Unbound Host Overrides
- Unbound Host Aliases

### Valid Environment Variables
* OPN_API_KEY
* OPN_API_SECRET
* OPN_API_SCHEME
* OPN_API_HOST
* OPN_API_PORT
* OPN_API_CA_PATH
* OPN_API_CA_CONTENT

### Example Script
```python
import json
from opnsense_api import Opnsense
from opnsense_api.util import AliasType

# Create an instance of the Opnsense class
opnsense = Opnsense(api_key="my_opnsense_api_key",
                    api_secret="my_opnsense_api_secret",
                    host="192.168.1.1",
                    ca_path="/path/to/opnsense/ca/cert_bundle.pem")

# Get the alias controller
alias = opnsense.firewall.alias_controller

# The values for the example alias
example_alias_name = "foo_bar"
example_alias_description = "This is the description for foo_bar"
example_alias_type = AliasType.PORT

# List all the aliases
print("LIST ALIASES")
list_output = alias.list()
print(json.dumps(list_output))

# Add a new alias to the Opnsense device
# This will return an object that represents the new alias.
print("ADD ALIAS")
add_output = alias.add_alias(name=example_alias_name, description=example_alias_description, alias_type=example_alias_type)
print(json.dumps(add_output))

# Get an alias by UUID
print("GET ALIAS")
get_output = alias.get(add_output['uuid'])
print(json.dumps(get_output))

# Get the UUID of an alias for the given alias name
# This outputs a string that contains the alias UUID
print("GET ALIAS UUID")
lookup_output_uuid =alias.get_uuid(get_output["name"])
print(lookup_output_uuid)

# An updated description for the example alias
updated_example_alias_description = "This is the description for foo_bar"

# Update an alias 
print("UPDATE ALIAS")
update_output = alias.set(uuid=lookup_output_uuid, name=example_alias_name, description=updated_example_alias_description, alias_type=example_alias_type)
print(json.dumps(update_output))

# Toggle an aliases enabled state.
print("TOGGLE ALIAS")
toggle_output = alias.toggle(lookup_output_uuid)
print(json.dumps(toggle_output))

# Delete an unwanted alias.
print("DELETE ALIAS")
delete_output = alias.delete(lookup_output_uuid)
print(json.dumps(delete_output))
```

### Unbound DNS Example
```python
from opnsense_api import Opnsense


# Create an instance of the Opnsense class
opnsense = Opnsense(api_key="my_opnsense_api_key",
                    api_secret="my_opnsense_api_secret",
                    host="192.168.1.1",
                    ca_path="/path/to/opnsense/ca/cert_bundle.pem")

overridden_domain = "reverb.io"
nonexistent_domain = "fake-domain"

# Returns None because there is no configured override.
result = opnsense.unbound_dns.domain_controller.get(nonexistent_domain)
print(f"Get Result: {result}")

# Retuns a list of configured domain overrides 
result = opnsense.unbound_dns.domain_controller.list()
print(f"List Result: {result}")

found_domain = False
for domain_override in result:
    if domain_override['domain'] == overridden_domain:
        # Deletes the override for a specific domain
        result = opnsense.unbound_dns.domain_controller.delete(domain_override['uuid'])
        print(f"Delete Result: {result}")
        found_domain = True

if not found_domain:
    # Adds an override for a specific domain
    result = opnsense.unbound_dns.domain_controller.add(overridden_domain, "0.0.0.0", "foobarbaz", True)
    print(f"Add Result: {result}")
```