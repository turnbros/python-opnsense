from __future__ import annotations

from enum import Enum
from typing import Type

from deprecation import deprecated

from opnsense_api.util import ParsingError


def parse_selected_enum(api_response: dict,
                        search_str: str,
                        enum: Type[Enum]) -> Enum | None:
    """
    Used during parsing of an item.
    :param api_response: response from the OPNSense
    :param search_str: What key to search for in the api_response
    :param enum: Enum that return value should belong to
    :return: enum that match the api_response[search_str] and has 'selected' set to true
    """
    for key, val in api_response[search_str].items():
        if bool(val['selected']):
            return enum[key.upper()]
    return None


def parse_selected_keys(api_response: dict, search_str: str) -> list[str]:
    """
    Used during parsing of an item.
    :param api_response: response from the OPNSense
    :param search_str: What key to search for in api_response
    :return: every selected key in api_response[search_str] in a list
    """
    return [key for key in api_response[search_str] if bool(api_response[search_str][key]['selected'])]


@deprecated(deprecated_in="1.0.5", removed_in="1.1.0", details="Use newer parsing instead")
def parse_query_response_alias(alias):
    name = alias["name"]
    description = alias["description"]
    enabled = bool(int(alias['enabled']))

    counters = alias["counters"]
    updatefreq = alias["updatefreq"]

    parsed_alias_type = None
    for alias_type in alias["type"].keys():
        if alias["type"][alias_type]["selected"] == 1:
            parsed_alias_type = alias_type.upper()
            break

    parsed_alias_proto = None
    for alias_proto in alias["proto"].keys():
        if alias["proto"][alias_proto]["selected"] == 1:
            parsed_alias_proto = alias_proto.upper()
            break

    parsed_alias_content = []
    for alias_content in alias["content"].keys():
        if alias["content"][alias_content]["selected"] == 1:
            parsed_alias_content.append(alias["content"][alias_content]["value"])

    return {"name": name, "type": parsed_alias_type, "description": description, "updatefreq": updatefreq,
            "counters": counters, "proto": parsed_alias_proto, "content": parsed_alias_content, "enabled": enabled}


def parse_firewall_filter_search_results(search_results):
    for found_rule in search_results:
        try:
            found_rule['sequence'] = int(found_rule['sequence'])
        except Exception as error:
            raise ParsingError(None, found_rule, f"Failed to parse filter search result attribute sequence. {error}")

        try:
            found_rule['enabled'] = bool(int(found_rule['enabled']))
        except Exception as error:
            raise ParsingError(None, found_rule, f"Failed to parse filter search result attribute enabled. {error}")

    return search_results


def parse_firewall_filter_rule(filter_uuid, filter_rule):
    description = filter_rule["description"]
    source_net = filter_rule["source_net"]
    destination_net = filter_rule["destination_net"]

    try:
        if filter_rule["source_port"] == "":
            source_port = 0
        else:
            source_port = int(filter_rule["source_port"])
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['source_port'],
                           f"Failed to parse filter attribute source_port. {error}")

    try:
        if filter_rule["destination_port"] == "":
            destination_port = 0
        else:
            destination_port = int(filter_rule["destination_port"])
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['destination_port'],
                           f"Failed to parse filter attribute destination_port. {error}")

    try:
        sequence = int(filter_rule["sequence"])
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['sequence'], f"Failed to parse filter attribute sequence. {error}")

    try:
        enabled = bool(int(filter_rule['enabled']))
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['enabled'], f"Failed to parse filter attribute enabled. {error}")

    try:
        quick = bool(int(filter_rule['quick']))
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['quick'], f"Failed to parse filter attribute quick. {error}")

    try:
        log = bool(int(filter_rule['log']))
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['log'], f"Failed to parse filter attribute log. {error}")

    try:
        source_not = bool(int(filter_rule['source_not']))
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['source_not'],
                           f"Failed to parse filter attribute source_not. {error}")

    try:
        destination_not = bool(int(filter_rule['destination_not']))
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['destination_not'],
                           f"Failed to parse filter attribute destination_not. {error}")

    try:
        parsed_filter_rule_action = None
        for filter_rule_action in filter_rule["action"].keys():
            if bool(int(filter_rule["action"][filter_rule_action]["selected"])):
                parsed_filter_rule_action = filter_rule_action
                break
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['action'], f"Failed to parse filter action. {error}")

    try:
        parsed_filter_rule_interfaces = []
        for filter_rule_interface in filter_rule["interface"].keys():
            if bool(int(filter_rule["interface"][filter_rule_interface]["selected"])):
                parsed_filter_rule_interfaces.append(filter_rule_interface)
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['interface'], f"Failed to parse filter interface. {error}")

    try:
        parsed_filter_rule_direction = None
        for filter_rule_direction in filter_rule["direction"].keys():
            if bool(int(filter_rule["direction"][filter_rule_direction]["selected"])):
                parsed_filter_rule_direction = filter_rule_direction
                break
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['direction'], f"Failed to parse filter direction. {error}")

    try:
        parsed_filter_rule_ipprotocol = None
        for filter_rule_ipprotocol in filter_rule["ipprotocol"].keys():
            if bool(int(filter_rule["ipprotocol"][filter_rule_ipprotocol]["selected"])):
                parsed_filter_rule_ipprotocol = filter_rule_ipprotocol
                break
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['ipprotocol'], f"Failed to parse filter ipprotocol. {error}")

    try:
        parsed_filter_rule_protocol = None
        for filter_rule_protocol in filter_rule["protocol"].keys():
            if bool(int(filter_rule["protocol"][filter_rule_protocol]["selected"])):
                parsed_filter_rule_protocol = filter_rule_protocol
                break
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['protocol'], f"Failed to parse filter protocol. {error}")

    try:
        parsed_filter_rule_gateway = None
        for filter_rule_gateway in filter_rule["gateway"].keys():
            if bool(int(filter_rule["gateway"][filter_rule_gateway]["selected"])):
                parsed_filter_rule_gateway = filter_rule_gateway
                if parsed_filter_rule_gateway == "":
                    parsed_filter_rule_gateway = None
                break
    except Exception as error:
        raise ParsingError(filter_uuid, filter_rule['gateway'], f"Failed to parse filter gateway. {error}")

    return {"uuid": filter_uuid, "sequence": sequence, "description": description, "enabled": enabled, "quick": quick,
            "log": log, "source_net": source_net, "source_not": source_not, "source_port": source_port,
            "destination_net": destination_net, "destination_not": destination_not,
            "destination_port": destination_port,
            "action": parsed_filter_rule_action, "interface": parsed_filter_rule_interfaces,
            "direction": parsed_filter_rule_direction, "ipprotocol": parsed_filter_rule_ipprotocol,
            "protocol": parsed_filter_rule_protocol, "gateway": parsed_filter_rule_gateway}
