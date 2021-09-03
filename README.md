# python-opnsense
A Python library for the Opnsense API

## Getting Started

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
list_output = alias.list_aliases()
print(json.dumps(list_output))

# Add a new alias to the Opnsense device
# This will return an object that represents the new alias.
print("ADD ALIAS")
add_output = alias.add_alias(name=example_alias_name, description=example_alias_description, alias_type=example_alias_type)
print(json.dumps(add_output))

# Get an alias by UUID
print("GET ALIAS")
get_output = alias.get_alias(add_output['uuid'])
print(json.dumps(get_output))

# Get the UUID of an alias for the given alias name
# This outputs a string that contains the alias UUID
print("GET ALIAS UUID")
lookup_output_uuid =alias.get_alias_uuid(get_output["name"])
print(lookup_output_uuid)

# An updated description for the example alias
updated_example_alias_description = "This is the description for foo_bar"

# Update an alias 
print("UPDATE ALIAS")
update_output = alias.set_alias(uuid=lookup_output_uuid, name=example_alias_name, description=updated_example_alias_description, alias_type=example_alias_type)
print(json.dumps(update_output))

# Toggle an aliases enabled state.
print("TOGGLE ALIAS")
toggle_output = alias.toggle_alias(lookup_output_uuid)
print(json.dumps(toggle_output))

# Delete an unwanted alias.
print("DELETE ALIAS")
delete_output = alias.delete_alias(lookup_output_uuid)
print(json.dumps(delete_output))
```