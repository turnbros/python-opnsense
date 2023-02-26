from pydantic import constr

from opnsense_api.util.applicable_item_controller import OPNSenseApplicableItemController
from opnsense_api.util.item_controller import OPNSenseItem


class LoopbackInterface(OPNSenseItem):
    description: constr(min_length=1, max_length=255)
    deviceId: int

    @classmethod
    def from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNSenseItem:
        return LoopbackInterface.parse_obj({"uuid": uuid} | api_response)

    @classmethod
    def from_api_response_list(cls, api_response: dict, **kwargs) -> OPNSenseItem:
        return LoopbackInterface.parse_obj(api_response)

    def get_api_name(self):
        return "loopback"


class LoopbackController(OPNSenseApplicableItemController[LoopbackInterface]):

    @property
    def opnsense_item_class(self) -> type[LoopbackInterface]:
        return LoopbackInterface

    def __init__(self, device):
        super().__init__(device, "interfaces", "loopback_settings")
