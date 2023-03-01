from typing import Union

from pydantic import conint, Field

from ..util.applicable_item_controller import OPNsenseApplicableItemController
from ..util.item_controller import OPNsenseItem
from ..util.parse import parse_selected_keys


class VXLAN(OPNsenseItem):
    deviceId: Union[int, None] = None
    device: str = Field(default="", alias="vxlandev")
    multicast_group: str = Field(default="", alias="vxlangroup")
    vni: conint(gt=-1, lt=16777216) = Field(alias="vxlanid")
    source: str = Field(alias="vxlanlocal")
    remote: str = Field(default="", alias="vxlanremote")

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return VXLAN(
            uuid=uuid,
            deviceId=int(api_response["deviceId"]),
            vxlandev=parse_selected_keys(api_response["vxlandev"]),
            vxlangroup=api_response["vxlangroup"],
            vxlanid=api_response["vxlanid"],
            vxlanlocal=api_response["vxlanlocal"],
            vxlanremote=api_response["vxlanremote"]
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        return VXLAN.parse_obj(api_response)


class VXLANController(OPNsenseApplicableItemController[VXLAN]):

    @property
    def opnsense_item_class(self) -> type[VXLAN]:
        return VXLAN

    def __init__(self, device):
        super().__init__(device, "interfaces", "vxlan_settings")
