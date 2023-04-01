from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import constr

from opnsense_api.util import ProtocolType
from opnsense_api.util.applicable_item_controller import OPNsenseApplicableItemController
from opnsense_api.util.item_controller import OPNsenseItem
from opnsense_api.util.parse import parse_selected_enum, parse_selected_keys


class AliasType(Enum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"
    URL_TABLE = "urltable"
    GEO_IP = "geoip"
    NETWORK_GROUP = "networkgroup"
    MAC = "mac"
    BGP_ASN = "asn"
    DYNAMIC_IPV6_HOST = "dynipv6host"
    INTERNAL = "internal"
    EXTERNAL = "external"


ALIAS_LONG_NAME_TO_TYPE_DICT: dict[str, AliasType] = {
    "Host(s)": AliasType.HOST,
    "Network(s)": AliasType.NETWORK,
    "Port(s)": AliasType.PORT,
    "URL (IPs)": AliasType.URL,
    "URL Table (IPs)": AliasType.URL_TABLE,
    "GeoIP": AliasType.GEO_IP,
    "Network group": AliasType.NETWORK_GROUP,
    "MAC address": AliasType.MAC,
    "BGP ASN": AliasType.BGP_ASN,
    "Dynamic IPv6 Host": AliasType.DYNAMIC_IPV6_HOST,
    "Internal (automatic)": AliasType.INTERNAL,
    "External (advanced)": AliasType.EXTERNAL
}


class Alias(OPNsenseItem):
    name: constr(min_length=1, max_length=32, strip_whitespace=True, regex=r"^[a-zA-Z0-9_]*$")
    type: AliasType
    description: Optional[constr(min_length=0, max_length=255)] = None
    updatefreq: Optional[str]
    counters: Optional[str]
    proto: Optional[ProtocolType] = None
    content: Optional[list[str]] = None
    enabled: bool = True
    categories_uuids: list[str] = []

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> Alias:
        return Alias(
            uuid=uuid,
            name=api_response['name'],
            type=AliasType(parse_selected_keys(api_response['type'])[0]),
            description=api_response['description'],
            updatefreq=api_response['updatefreq'],
            counters=api_response['counters'],
            proto=parse_selected_enum(api_response['proto'], ProtocolType),
            content=parse_selected_keys(api_response['content']),
            enabled=bool(int(api_response['enabled'])),
            categories_uuids=parse_selected_keys(api_response['categories'])
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> Alias:
        return Alias(
            uuid=api_response['uuid'],
            name=api_response['name'],
            type=ALIAS_LONG_NAME_TO_TYPE_DICT[api_response['type']],
            description=api_response['description'],
            updatefreq=api_response.get('updatefreq'),
            counters=api_response.get('counters'),
            proto=ProtocolType[api_response.get('proto').upper()] if api_response.get('proto') else None,
            content=api_response['content'].split(','),
            enabled=bool(int(api_response['enabled'])),
            categories_uuids=api_response['categories_uuid']
        )


class FirewallAliasController(OPNsenseApplicableItemController[Alias]):
    class _ItemActions(Enum):
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

    def get_uuid(self, name: str) -> Optional[str]:
        query_response = self._api_get(self._ItemActions.get_uuid.value, name)
        return query_response.get('uuid')
