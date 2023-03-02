from __future__ import annotations

from enum import Enum
from typing import Type, Union


def parse_int(api_response_part: str) -> Union[int, None]:
    """
    Used during parsing of an item
    :param api_response_part: value of api response that is to be parsed to int
    :return: integer value of api_response_part contains int, else None
    """
    return int(api_response_part) if api_response_part else None


def parse_selected_enum(api_response_part: dict, enum: Type[Enum]) -> Enum | None:
    """
    Used during parsing of an item.
    :param api_response_part: response part to search in
    :param enum: Enum that return value should belong to
    :return: enum that match the api_response_part and has 'selected' set to true
    """
    for key, val in api_response_part.items():
        if bool(val['selected']):
            return enum[key.upper()]
    return None


def parse_selected_keys(api_response_part: dict) -> list[str]:
    """
    Used during parsing of an item.
    :param api_response_part: response part to search in
    :return: every selected key in api_response_part in a list
    """
    return [key for key in api_response_part if bool(api_response_part[key]['selected'])]
