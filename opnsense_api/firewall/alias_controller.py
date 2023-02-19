from typing import Union

from deprecation import deprecated

from opnsense_api.util import AliasType, ProtocolType
from opnsense_api.util.parse import parse_query_response_alias


class Alias(object):

    def __init__(self, device):
        self.device = device

      def list(self) -> list:
        return self.list_aliases()

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use list instead")
    def list_aliases(self) -> list:
        search_results = self.device._authenticated_request("GET", f"firewall/alias/searchItem")
        if 'rows' in search_results:
            return search_results['rows']
        return []

    def get(self, uuid: str) -> dict:
        return self.get_alias(uuid)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use get instead")
    def get_alias(self, uuid: str) -> dict:
        query_response = self.device._authenticated_request("GET", f"firewall/alias/getItem/{uuid}")
        if 'alias' in query_response:
            try:
                return parse_query_response_alias(query_response['alias'])
            except Exception as error:
                raise Exception(f"Failed to parse the alias wuth UUID: {uuid}\nException: {error.with_traceback()}")

    def get_uuid(self, name: str) -> Union[str, None]:
        return self.get_alias_uuid(name)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use get_uuid instead")
    def get_alias_uuid(self, name: str) -> Union[str, None]:
        search_results = self.device._authenticated_request("GET", f"firewall/alias/getAliasUUID/{name}")
        if 'uuid' in search_results:
            return search_results['uuid']
        return None

    def toggle(self, uuid, enabled=None):
        return self.toggle_alias(uuid, enabled)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use toggle instead")
    def toggle_alias(self, uuid, enabled=None):
        if enabled is None:
            enabled = bool(int(self.get_alias(uuid)['enabled']))
        return self.device._authenticated_request("POST", f"firewall/alias/toggleItem/{uuid}?enabled={not enabled}")

    def delete(self, uuid):
        return self.delete_alias(uuid)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use delete instead")
    def delete_alias(self, uuid):
        return self.device._authenticated_request("POST", f"firewall/alias/delItem/{uuid}")

    def add(self,
            name: str,
            alias_type: AliasType,
            description: str = "",
            update_freq: str = "",
            counters: str = "",
            proto: ProtocolType = None,
            content=None,
            enabled: bool = True
            ):
        if content is None:
            content = []
        
        return self.add_alias(
            name=name,
            alias_type=alias_type,
            description=description,
            update_freq=update_freq,
            counters=counters,
            proto=proto,
            content=content,
            enabled=enabled
        )

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use add instead")
    def add_alias(self,
                  name: str,
                  alias_type: AliasType,
                  description: str = "",
                  update_freq: str = "",
                  counters: str = "",
                  proto: ProtocolType = None,
                  content=None,
                  enabled: bool = True
                  ):

        if content is None:
            content = []

        protocol_type = ""
        if proto is not None:
            protocol_type = proto.value

        alias_content = ""
        if len(content) > 0:
            content = [str(item) for item in content]
            alias_content = "\n".join(content)

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
        return self.device._authenticated_request("POST", f"firewall/alias/addItem", body=request_body)

    def set(self,
            uuid: str,
            name: str,
            alias_type: AliasType,
            description: str = "",
            update_freq: str = "",
            counters: str = "",
            proto: ProtocolType = None,
            content=None,
            enabled: bool = True
            ):
        return self.set_alias(
            uuid=uuid,
            name=name,
            alias_type=alias_type,
            description=description,
            update_freq=update_freq,
            counters=counters,
            proto=proto,
            content=content,
            enabled=enabled
        )

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use set instead")
    def set_alias(self,
                  uuid: str,
                  name: str,
                  alias_type: AliasType,
                  description: str = "",
                  update_freq: str = "",
                  counters: str = "",
                  proto: ProtocolType = None,
                  content=None,
                  enabled: bool = True
                  ):

        protocol_type = ""
        if proto is not None:
            protocol_type = proto.value

        alias_content = ""
        if content is not None:
            if len(content) > 0:
                content = [str(item) for item in content]
                alias_content = "\n".join(content)

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
        return self.device._authenticated_request("POST", f"firewall/alias/setItem/{uuid}", body=request_body)
