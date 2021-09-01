import json
from .. import Opnsense, Constants

class Alias(object):

  def __init__(self, device: Opnsense):
    self.device = device

  # POST
  def add_alias(self):
    "firewall/alias/addItem"
    pass

  # GET
  def list_aliases(self):
    "firewall/alias/searchItem"
    pass

  # GET
  def get_alias(self, uuid: str) -> dict:
    path = f"firewall/alias/getItem/{uuid}"
    query_response = self.device.authenticated_request("GET", path)

    if query_response.status not in Constants.HTTP_SUCCESS:
      raise Exception(f"Failed to get alias with uuid: {uuid}")

    return json.load(query_response)


  # GET
  def get_alias_uuid(self):
    "firewall/alias/getAliasUUID/tbc_tenant_test_tenant_1"
    pass

  # POST
  def set_alias(self, **kwargs):
    "firewall/alias/setItem/16b6fafb-7b83-42df-9797-0be2db437f2e"
    """
    {
    "alias": {
        "enabled": "1",
        "name": "tbc_tenant_test_tenant_1",
        "description": "",
        "updatefreq": "",
        "counters": "",
        "type": "port",
        "proto": "",
        "content": "tbc_29LA2A"
    }
    }
    """
    pass

#  POST
#  def toggle_alias(self):
#    pass

  # POST
  def delete_alias(self):
    "firewall/alias/delItem"
    pass
