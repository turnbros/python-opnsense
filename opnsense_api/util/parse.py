from __future__ import annotations

from enum import Enum
from typing import Type


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


def parse_selected_keys(api_response_part: dict) -> list[str]:
    """
    Used during parsing of an item.
    :param api_response_part: response part to search in
    :return: every selected key in api_response[search_str] in a list
    """
    return [key for key in api_response_part if bool(api_response_part[key]['selected'])]
