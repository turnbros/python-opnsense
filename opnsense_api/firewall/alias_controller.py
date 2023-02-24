from __future__ import annotations

from enum import Enum
from typing import Optional, Union

from pydantic import validator, constr

from opnsense_api.util import ProtocolType
from opnsense_api.util.applicable_item_controller import OPNSenseApplicableItemController
from opnsense_api.util.exceptions import FailedToParseItemException, InvalidItemException
from opnsense_api.util.item_controller import OPNSenseItem
from opnsense_api.util.parse import parse_selected_enum, parse_selected_keys

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
    type: constr(to_lower=True)
    description: Union[None, constr(min_length=0, max_length=255)] = None
    updatefreq: Union[str, None]
    counters: Union[str, None]
    proto: Union[ProtocolType, None] = None
    content: Optional[list[str]] = None
    enabled: bool = True
    categories_uuids: list[str] = []

    @validator("type", pre=True, always=True)
    def type_valid(cls, value: str) -> str:
        if value not in LONG_NAME_TO_TYPE_DICT.values():
            raise InvalidItemException("Alias", field="type", value=value,
                                       valid_values=list(LONG_NAME_TO_TYPE_DICT.values()))
        return value

    @classmethod
    def from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> Alias:
        return Alias(
            uuid=uuid,
            name=api_response['name'],
            type=parse_selected_keys(api_response['type'])[0],  # will always only be one
            description=api_response['description'],
            updatefreq=api_response['updatefreq'],
            counters=api_response['counters'],
            proto=parse_selected_enum(api_response, 'proto', ProtocolType),
            content=parse_selected_keys(api_response['content']),
            enabled=bool(int(api_response['enabled'])),
            categories_uuids=parse_selected_keys(api_response['categories'])
        )

    @classmethod
    def from_api_response_list(cls, api_response: dict, uuid: Optional[str] = None, **kwargs):
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
    def opnsense_item_class(self) -> type[Alias]:
        return Alias

    def __init__(self, device):
        super().__init__(device, "firewall", "alias")

    def list(self) -> list[OPNSenseItem]:
        query_response = self._api_get(self.ItemActions.search.value)
        return [self.opnsense_item_class.from_api_response_list(item, uuid=item['uuid'])
                for item in query_response.get('rows')]

    def get_uuid(self, name: str) -> Union[str, None]:
        query_response = self._api_get(self.ItemActions.get_uuid.value, name)
        return query_response.get('uuid')
