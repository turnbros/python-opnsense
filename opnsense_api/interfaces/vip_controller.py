from enum import Enum
from typing import Optional

from pydantic import constr, conint, validator, SecretStr, root_validator, Field

from ..util.applicable_item_controller import OPNsenseApplicableItemController
from ..util.exceptions import InvalidItemException
from ..util.item_controller import OPNsenseItem
from ..util.parse import parse_selected_keys, parse_int


class VIPMode(Enum):
    IPALIAS = "ipalias"
    CARP = "carp"
    PROXYARP = "proxyarp"
    OTHER = "other"


VIP_LONG_NAME_TO_MODE_DICT: dict[str, VIPMode] = {
    "IP Alias": VIPMode.IPALIAS,
    "CARP": VIPMode.CARP,
    "Proxy ARP": VIPMode.PROXYARP,
    "Other": VIPMode.OTHER
}


class VIP(OPNsenseItem):
    interface: constr(to_lower=True) = "wan"
    mode: VIPMode = VIPMode.IPALIAS
    subnet: str
    subnet_bits: conint(lt=33)
    vhid: Optional[conint(gt=0, lt=256)] = None
    advbase: conint(gt=0, lt=255) = 1
    advskew: conint(gt=-1, lt=255) = 0
    description: str = Field(default="", alias="descr")
    gateway: str = ""
    noexpand: bool = False
    nobind: bool = False
    password: SecretStr = SecretStr("")

    def _get_api_representation(self) -> dict:
        d = super()._get_api_representation()
        if d["vip"].get("password"):
            d["vip"]["password"] = d["vip"]["password"].get_secret_value()
        return d

    @root_validator
    def fields_can_be_defined_together(cls, values: dict) -> dict:
        if values["mode"] is VIPMode.CARP and not values["password"]:
            raise InvalidItemException(cls.__name__,
                                       custom_message=f"Mode CARP requires a password to be set.")

        carp_ipalias_exclusive_keys = ["vhid", "nobind"]
        if values["mode"] is not VIPMode.CARP and values["mode"] is not VIPMode.IPALIAS:
            if any(values[key] for key in carp_ipalias_exclusive_keys):
                raise InvalidItemException(cls.__name__,
                                           custom_message=f"Values for {carp_ipalias_exclusive_keys} can only be set "
                                                          f"when mode is CARP or IPALIAS, "
                                                          f"but is {values['mode'].name}")

        if values["mode"] is VIPMode.CARP and not values["vhid"]:
            raise InvalidItemException(cls.__name__, custom_message="Mode CARP requires a VHID to be set.")

        if values["noexpand"] and not values["mode"] is VIPMode.PROXYARP:
            raise InvalidItemException(cls.__name__, custom_message="'noexpand' can only be set "
                                                                    "when mode is PROXYARP.")

        return values

    @validator("subnet")
    def subnet_valid(cls, v: str) -> str:
        if "/" in v:
            raise InvalidItemException("VIP", custom_message="Please provide subnet with subnet_bits")
        return v

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return VIP(
            uuid=uuid,
            interface=parse_selected_keys(api_response["interface"])[0],
            mode=parse_selected_keys(api_response["mode"])[0],
            subnet=api_response["network"].split('/')[0],
            subnet_bits=api_response["network"].split('/')[1],
            vhid=parse_int(api_response["vhid"]),
            advbase=int(api_response["advbase"]),
            advskew=int(api_response["advskew"]),
            descr=api_response["descr"],
            gateway=api_response["gateway"],
            noexpand=bool(int(api_response["noexpand"])),
            nobind=bool(int(api_response["nobind"])),
            password=api_response["password"]
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        raise NotImplementedError("This method is not implemented!")


class VIPController(OPNsenseApplicableItemController[VIP]):

    @property
    def _opnsense_item_class(self) -> type[VIP]:
        return VIP

    def __init__(self, device):
        super().__init__(device, "interfaces", "vip_settings")

    def list(self) -> list[VIP]:
        query_response = self._api_post(self._ItemActions.search.value)
        return [self.get(row["uuid"]) for row in query_response.get('rows')]
