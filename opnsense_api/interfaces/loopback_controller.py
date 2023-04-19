from pydantic import constr

from opnsense_api.util.applicable_item_controller import OPNsenseApplicableItemController
from opnsense_api.util.item_controller import OPNsenseItem


class LoopbackInterface(OPNsenseItem):
    """
    A OPNsense device loopback network interface.

    """

    description: constr(min_length=1, max_length=255)
    deviceId: int

    def _get_api_name(self):
        return "loopback"


class LoopbackController(OPNsenseApplicableItemController[LoopbackInterface]):

    @property
    def _opnsense_item_class(self) -> type[LoopbackInterface]:
        return LoopbackInterface

    def __init__(self, device):
        super().__init__(device, "interfaces", "loopback_settings")
