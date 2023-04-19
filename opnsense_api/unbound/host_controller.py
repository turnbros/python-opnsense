from enum import Enum
from typing import Optional

from pydantic import root_validator, validator

from .resource_controller import UnboundResourceController
from ..util.exceptions import InvalidItemException
from ..util.item_controller import OPNsenseItem
from ..util.parse import parse_int, parse_selected_enum


class UnboundResourceRecordType(Enum):
    A = "A"
    AAAA = "AAAA"
    MX = "MX"


UNBOUND_RR_LONG_NAME_TO_TYPE_DICT: dict[str, UnboundResourceRecordType] = {
    "A (IPv4 address)": UnboundResourceRecordType.A,
    "AAAA (IPv6 address)": UnboundResourceRecordType.AAAA,
    "MX (Mail server)": UnboundResourceRecordType.MX
}


class HostOverride(OPNsenseItem):
    enabled: bool = True
    hostname: str
    domain: str
    rr: UnboundResourceRecordType = UnboundResourceRecordType.A
    mxprio: Optional[int] = None
    mx: str = ""
    server: str = ""
    description: str = ""

    @root_validator
    def __fields_can_be_defined_together(cls, values):
        if values["rr"] != UnboundResourceRecordType.MX and (values["mx"] or values["mxprio"]):
            raise InvalidItemException(cls.__name__, custom_message="Fields mx and mxprio require RR to be MX.")
        if values["rr"] != UnboundResourceRecordType.MX and not values["server"]:
            raise InvalidItemException(cls.__name__, custom_message="Field server is required for A and AAAA RRs.")
        if values["rr"] == UnboundResourceRecordType.MX and values["server"]:
            raise InvalidItemException(cls.__name__, custom_message="Field server can't be set with RR MX.")
        if values["rr"] == UnboundResourceRecordType.MX and not (values["mx"] or values["mxprio"]):
            raise InvalidItemException(cls.__name__, custom_message="Fields mx and mxprio need to be set with RR MX.")
        return values

    @validator("mxprio")
    def mxprio_valid(cls, v) -> Optional[int]:
        if isinstance(v, int):
            if v == 0:
                raise InvalidItemException(cls.__name__, custom_message="mxprio can't be 0.")
        return v

    def _get_api_name(self):
        return "host"

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return HostOverride(
            uuid=uuid,
            enabled=bool(int(api_response["enabled"])),
            hostname=api_response["hostname"],
            domain=api_response["domain"],
            rr=parse_selected_enum(api_response["rr"], UnboundResourceRecordType),
            mxprio=parse_int(api_response["mxprio"]),
            mx=api_response["mx"],
            server=api_response["server"],
            description=api_response["description"]
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        return HostOverride(
            uuid=api_response["uuid"],
            enabled=bool(int(api_response["enabled"])),
            hostname=api_response["hostname"],
            domain=api_response["domain"],
            rr=UNBOUND_RR_LONG_NAME_TO_TYPE_DICT[api_response["rr"]],
            mxprio=parse_int(api_response["mxprio"]),
            mx=api_response["mx"],
            server=api_response["server"],
            description=api_response["description"]
        )


class HostController(UnboundResourceController[HostOverride]):
    class _ItemActions(Enum):
        search = "searchHostOverride"
        get = "getHostOverride"
        add = "addHostOverride"
        set = "setHostOverride"
        delete = "delHostOverride"
        apply = "reconfigure"

    @property
    def _opnsense_item_class(self) -> type[HostOverride]:
        return HostOverride
