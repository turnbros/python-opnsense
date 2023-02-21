from __future__ import annotations

from enum import Enum
from typing import Union, List

from deprecation import deprecated
from pydantic import validator, constr

from opnsense_api.util import ProtocolType
from opnsense_api.util.applicable_item_controller import OPNSenseApplicableItemController
from opnsense_api.util.exceptions import FailedToParseItemException, ItemNotFoundException, InvalidItemException
from opnsense_api.util.item_controller import OPNSenseItem, TOPNSenseItem
from opnsense_api.util.parse import parse_selected_enum, parse_selected_keys, parse_query_response_alias

LONG_NAME_TO_TYPE_DICT = {
    "Host(s)": "host",
    "Network(s)": "network",
    "Port(s)": "port",
    "URL (IPs)": "url",
    "URL Table (IPs)": "urltable",
    "GeoIP": "geoip",
    "Network group": "networkgroup",
    "MAC address": "mac",
    "BGP ASN": "asn",
    "Dynamic IPv6 Host": "dynipv6host",
    "Internal (automatic)": "internal",
    "External (advanced)": "external"
}


class Alias(OPNSenseItem):
    name: constr(min_length=1, max_length=32, strip_whitespace=True, regex=r"^[a-zA-Z0-9_]*$")
    type: str
    description: str = ""
    updatefreq: Union[str, None]
    counters: Union[str, None]
    proto: Union[ProtocolType, None] = None
    content: list[str] = None
    enabled: bool = True
    categories_uuids: list[str] = []

    @validator("type", pre=True, always=True)
    def type_valid(cls, value: str) -> str:
        value = value.lower()
        if value not in LONG_NAME_TO_TYPE_DICT.values():
            raise InvalidItemException("Alias", "type", value, list(LONG_NAME_TO_TYPE_DICT.values()))
        return value

    @classmethod
    def from_api_response_get(cls, api_response: dict, uuid: str = None, **kwargs) -> Alias:
        # API response doesn't contain UUID for aliases.
        if uuid is None:
            raise FailedToParseItemException("Alias", "Can't parse alias if no UUID is passed.")

        return Alias(
            uuid=uuid,
            name=api_response['name'],
            type=parse_selected_keys(api_response, 'type')[0],  # will always only be one
            description=api_response['description'],
            updatefreq=api_response['updatefreq'],
            counters=api_response['counters'],
            proto=parse_selected_enum(api_response, 'proto', ProtocolType),
            content=parse_selected_keys(api_response, 'content'),
            enabled=bool(int(api_response['enabled'])),
            categories_uuids=parse_selected_keys(api_response, 'categories')
        )

    @classmethod
    def from_api_response_list(cls, api_response: dict, uuid: str = None, **kwargs):
        # API response doesn't contain UUID for aliases.
        if uuid is None:
            raise FailedToParseItemException("Alias", "Can't parse alias if no UUID is passed.")
        return Alias(
            uuid=uuid,
            name=api_response['name'],
            type=LONG_NAME_TO_TYPE_DICT[api_response['type']],
            description=api_response['description'],
            updatefreq=api_response.get('updatefreq'),
            counters=api_response.get('counters'),
            proto=ProtocolType[api_response.get('proto').upper()] if api_response.get('proto') else None,
            content=api_response['content'].split(','),
            enabled=bool(int(api_response['enabled'])),
            categories_uuids=api_response['categories_uuid']
        )

    def get_api_representation(self) -> dict:
        api_representation = super().get_api_representation()
        api_representation['alias']['content'] = str.join('\n', self.content)
        return self._strip_none_fields(api_representation)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use newer methods instead")
    class AliasType(Enum):
        HOST = "host"
        NETWORK = "network"
        PORT = "port"
        URL = "url"


class FirewallAliasController(OPNSenseApplicableItemController[Alias]):
    class ItemActions(Enum):
        search = "searchItem"
        get = "getItem"
        add = "addItem"
        set = "setItem"
        delete = "delItem"
        apply = "reconfigure"
        get_uuid = "getAliasUUID"

    @property
    def opnsense_item_class(self) -> type[TOPNSenseItem]:
        return Alias

    def __init__(self, device):
        super().__init__(device, "firewall", "alias")

    def list(self) -> List[Alias]:
        query_response = self._api_get(self.ItemActions.search.value)
        return [self.opnsense_item_class.from_api_response_list(item, uuid=item['uuid'])
                for item in query_response.get('rows')]

    def get(self, uuid) -> Alias:
        query_response = self._api_get(self.ItemActions.get.value, uuid)
        if len(query_response.values()) == 0 or len(query_response.values()) > 1:
            raise ItemNotFoundException(type(TOPNSenseItem).__name__, uuid, query_response)
        return self.opnsense_item_class.from_api_response_get(list(query_response.values())[0], uuid=uuid)

    def get_uuid(self, name: str) -> Union[str, None]:
        query_response = self._api_get(self.ItemActions.get_uuid.value, name)
        return query_response.get('uuid')

    # DEPRECATED METHODS BELOW

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use list instead")
    def list_aliases(self) -> List[Alias]:
        return self.list()

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use get instead")
    def get_alias(self, uuid: str) -> dict:
        query_response = self._device._authenticated_request("GET", f"firewall/alias/getItem/{uuid}")
        if 'alias' in query_response:
            try:
                return parse_query_response_alias(query_response['alias'])
            except Exception as error:
                raise Exception(f"Failed to parse the alias with UUID: {uuid}\nException: {error}")

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use get_uuid instead")
    def get_alias_uuid(self, name: str) -> Union[str, None]:
        return self.get_uuid(name)

    @deprecated(details="Use set instead")
    def toggle(self, uuid, enabled=None):
        return self.toggle_alias(uuid, enabled)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use toggle instead")
    def toggle_alias(self, uuid, enabled=None):
        if enabled is None:
            enabled = bool(int(self.get_alias(uuid)['enabled']))
        return self._device._authenticated_request("POST", f"firewall/alias/toggleItem/{uuid}?enabled={not enabled}")

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use delete instead")
    def delete_alias(self, uuid):
        return self._device._authenticated_request("POST", f"firewall/alias/delItem/{uuid}")

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use add instead")
    def add_alias(self,
                  name: str,
                  alias_type: Alias.AliasType,
                  description: str,
                  update_freq: str,
                  counters: str,
                  proto: ProtocolType = None,
                  content=None,
                  enabled: bool = True,
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
        return self._device._authenticated_request("POST", f"firewall/alias/addItem", body=request_body)

    @deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use set instead")
    def set_alias(self,
                  uuid: str,
                  name: str,
                  alias_type: Alias.AliasType,
                  description: str,
                  update_freq: str,
                  counters: str,
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
        return self._device._authenticated_request("POST", f"firewall/alias/setItem/{uuid}", body=request_body)
