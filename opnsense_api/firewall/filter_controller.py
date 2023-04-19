from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import constr, conint, root_validator, validator, conlist

from opnsense_api.util.applicable_item_controller import OPNsenseApplicableItemController
from opnsense_api.util.exceptions import InvalidItemException, FailedToApplyChangesException
from opnsense_api.util.item_controller import OPNsenseItem
from opnsense_api.util.parse import parse_selected_keys

"""
This requires the os-firewall plugin to be installed.
"""


class FilterRule(OPNsenseItem):
    enabled: bool = True
    sequence: conint(gt=0, lt=100000)
    description: constr(min_length=0, max_length=255) = ""
    action: constr(to_lower=True) = "pass"
    quick: bool = True
    interface: conlist(item_type=str, min_items=1, unique_items=True) = ["lan"]
    direction: constr(to_lower=True) = "in"
    ipprotocol: constr(to_lower=True) = "inet"
    protocol: constr(to_lower=True) = "any"
    source_net: constr(min_length=1, max_length=32) = "any"  # max length from alias name max length
    source_not: bool = False
    source_port: Optional[str] = None
    destination_net: constr(min_length=1, max_length=32) = "any"  # max length from alias name max length
    destination_not: bool = False
    destination_port: Optional[str] = None
    gateway: constr(to_lower=True) = ""
    log: bool = False

    # We don't validate every field here, as some fields require e.g. a gateway or interface to exist.
    # The call will just fail with an exception, containing the reason if the selected value(s) are wrong.
    @root_validator
    def ports_only_defined_when_tcp_or_udp(cls, values: dict) -> dict:
        """
        Validates source_port and dest_port are only defined when tcp or udp is chosen
        :param values: values to be assigned to object
        :return: values if all checks pass
        """
        if (values["source_port"] or values["destination_port"]) and values["protocol"] not in ["udp", "tcp"]:
            raise InvalidItemException("FilterRule",
                                       custom_message="'source_port' and 'destination_port' can only be set when "
                                                      "'protocol' is either 'udp' or 'tcp'.")
        return values

    @validator("action")
    def action_valid(cls, v: str) -> str:
        if v not in ["pass", "block", "reject"]:
            raise InvalidItemException("FilterRule", field="action", value=v, valid_values=["pass", "block", "reject"])
        return v

    @validator("direction")
    def direction_valid(cls, v: str) -> str:
        if v not in ["in", "out"]:
            raise InvalidItemException("FilterRule", field="direction", value=v, valid_values=["in", "out"])
        return v

    @validator("ipprotocol")
    def ipprotocol_valid(cls, v: str) -> str:
        if v not in ["inet", "inet6"]:
            raise InvalidItemException("FilterRule", field="ipprotocol", value=v, valid_values=["inet", "inet6"])
        return v

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return FilterRule(
            uuid=uuid,
            sequence=int(api_response['sequence']),
            enabled=bool(int(api_response['enabled'])),
            action=parse_selected_keys(api_response['action'])[0],
            quick=bool(int(api_response['quick'])),
            interface=parse_selected_keys(api_response['interface']),
            direction=parse_selected_keys(api_response['direction'])[0],
            ipprotocol=parse_selected_keys(api_response['ipprotocol'])[0],
            protocol=parse_selected_keys(api_response['protocol'])[0],
            source_net=api_response['source_net'],
            source_not=bool(int(api_response['source_not'])),
            source_port=api_response['source_port'] if api_response['source_port'] else None,
            destination_net=api_response['destination_net'],
            destination_not=bool(int(api_response['destination_not'])),
            destination_port=api_response['destination_port'] if api_response['source_port'] else None,
            gateway=parse_selected_keys(api_response['gateway'])[0]
            if parse_selected_keys(api_response['gateway'])[0] != "none" else "",
            log=bool(int(api_response['log'])),
            description=api_response['description']
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        raise NotImplementedError("This method is not implemented!")

    def _get_api_name(self):
        return "rule"


class FilterController(OPNsenseApplicableItemController[FilterRule]):
    class _ItemActions(Enum):
        search = "searchRule"
        get = "getRule"
        add = "addRule"
        set = "setRule"
        delete = "delRule"
        apply = "apply"

    def __init__(self, device):
        super().__init__(device, "firewall", "filter")

    @property
    def _opnsense_item_class(self) -> type[FilterRule]:
        return FilterRule

    def apply_changes(self) -> None:
        response = self._api_post(self._ItemActions.apply.value)
        if response["status"] != "OK\n\n":
            raise FailedToApplyChangesException(f"Failed to apply changes. Reason {response}")

    def list(self) -> List[FilterRule]:
        query_response = self._api_post(self._ItemActions.search.value)
        return [self.get(row["uuid"]) for row in query_response.get('rows')]
