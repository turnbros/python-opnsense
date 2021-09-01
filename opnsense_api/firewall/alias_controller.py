from typing import List

from opnsense_api.util import AliasType, ProtocolType


class Alias(object):

  def __init__(self, device):
    self.device = device

  def list_aliases(self) -> dict:
    search_results = self.device.authenticated_request("GET", f"firewall/alias/searchItem")
    if 'rows' in search_results:
      return search_results['rows']
    return []

  def get_alias(self, uuid: str) -> dict:
    return self.device.authenticated_request("GET", f"firewall/alias/getItem/{uuid}")['alias']

  def get_alias_uuid(self, name: str) -> str:
    search_results = self.device.authenticated_request("GET", f"firewall/alias/getAliasUUID/{name}")
    if 'uuid' in search_results:
      return search_results['uuid']
    return None

  def toggle_alias(self, uuid, enabled=None):
    if enabled is None:
      enabled = bool(int(self.get_alias(uuid)['enabled']))
    return self.device.authenticated_request("POST", f"firewall/alias/toggleItem/{uuid}?enabled={not enabled}")

  def delete_alias(self, uuid):
    return self.device.authenticated_request("POST", f"firewall/alias/delItem/{uuid}")

  def add_alias(self,
                name: str,
                alias_type: AliasType,
                description: str = "",
                update_freq: str = "",
                counters: str = "",
                proto: ProtocolType = None,
                content: List[str] = [],
                enabled: bool = True
                ):

    protocol_type = ""
    if proto is not None:
      protocol_type = proto.value

    alias_content = ""
    if len(content) > 0:
      "\n".join(content)

    request_body = {
      "alias": {
        "name": name,
        "type": alias_type.value,
        "description": description,
        "updatefreq": update_freq,
        "counters": counters,
        "proto": protocol_type,
        "content": alias_content,
        "enabled": str(int(enabled))
      }
    }
    return self.device.authenticated_request("POST", f"firewall/alias/addItem", body=request_body)


  def set_alias(self,
                uuid: str,
                name: str,
                alias_type: AliasType,
                description: str = "",
                update_freq: str = "",
                counters: str = "",
                proto: ProtocolType = None,
                content: List[str] = [],
                enabled: bool = True
                ):

    protocol_type = ""
    if proto is not None:
      protocol_type = proto.value

    alias_content = ""
    if len(content) > 0:
      "\n".join(content)

    request_body = {
      "alias": {
        "name": name,
        "type": alias_type.value,
        "description": description,
        "updatefreq": update_freq,
        "counters": counters,
        "proto": protocol_type,
        "content": alias_content,
        "enabled": str(int(enabled))
      }
    }
    return self.device.authenticated_request("POST", f"firewall/alias/setItem/{uuid}", body=request_body)
