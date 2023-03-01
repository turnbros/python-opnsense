from pydantic import constr

from opnsense_api.util.applicable_item_controller import OPNsenseApplicableItemController
from opnsense_api.util.item_controller import OPNsenseItem


class LoopbackInterface(OPNsenseItem):
    description: constr(min_length=1, max_length=255)
    deviceId: int

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return LoopbackInterface.parse_obj({"uuid": uuid} | api_response)

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        return LoopbackInterface.parse_obj(api_response)

    def _get_api_name(self):
        return "loopback"


class LoopbackController(OPNsenseApplicableItemController[LoopbackInterface]):

    @property
    def opnsense_item_class(self) -> type[LoopbackInterface]:
        return LoopbackInterface

    def __init__(self, device):
        super().__init__(device, "interfaces", "loopback_settings")
