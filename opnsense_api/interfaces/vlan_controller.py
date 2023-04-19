from enum import Enum

from pydantic import constr, conint, Field

from ..util.item_controller import OPNsenseItemController, OPNsenseItem
from ..util.parse import parse_selected_keys


class VLANPriority(Enum):
    BEST_EFFORT = "0"
    BACKGROUND = "1"
    EXCELLENT_EFFORT = "2"
    CRITICAL_APPLICATIONS = "3"
    VIDEO = "4"
    VOICE = "5"
    INTERNETWORK_CONTROL = "6"
    NETWORK_CONTROL = "7"


VLAN_LONG_NAME_TO_PRIORITY_DICT: dict[str, VLANPriority] = {
    "Best Effort (0, default)": VLANPriority.BEST_EFFORT,
    "Background (1, lowest)": VLANPriority.BACKGROUND,
    "Excellent Effort (2)": VLANPriority.EXCELLENT_EFFORT,
    "Critical Applications (3)": VLANPriority.CRITICAL_APPLICATIONS,
    "Video (4)": VLANPriority.VIDEO,
    "Voice (5)": VLANPriority.VOICE,
    "Internetwork Control (6)": VLANPriority.INTERNETWORK_CONTROL,
    "Network Control (7, highest)": VLANPriority.NETWORK_CONTROL
}


class VLAN(OPNsenseItem):
    """
    An OPNsense device VLAN.

    """

    device: str = Field(default="", alias="vlanif")
    parent: constr(to_lower=True, min_length=1) = Field(alias="if")
    tag: conint(gt=0, lt=4095, strict=True)
    priority: VLANPriority = Field(default=VLANPriority.BEST_EFFORT, alias="pcp")
    description: str = Field(default="", alias="descr")

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return VLAN(
            uuid=uuid,
            vlanif=api_response["vlanif"],
            parent=parse_selected_keys(api_response["if"])[0],
            tag=int(api_response["tag"]),
            pcp=VLANPriority(parse_selected_keys(api_response["pcp"])[0]),
            descr=api_response["descr"]
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        return VLAN(
            uuid=api_response["uuid"],
            vlanif=api_response["vlanif"],
            parent=api_response["if"].split(' ')[0],
            tag=int(api_response["tag"]),
            pcp=VLAN_LONG_NAME_TO_PRIORITY_DICT[api_response["pcp"]],
            descr=api_response["descr"]
        )


class VLANController(OPNsenseItemController[VLAN]):

    def __init__(self, device):
        super().__init__(device, "interfaces", "vlan_settings")

    @property
    def _opnsense_item_class(self) -> type[VLAN]:
        return VLAN

    def add(self, controller_item: VLAN) -> None:
        """
        Adds a new VLAN to an OPNsense device

        """
        super().add(controller_item)
        assert controller_item.uuid
        controller_item.device = self.get(controller_item.uuid).device  # get item again so correct device is set
