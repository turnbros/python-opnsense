from ..util.item_controller import OPNsenseItemController, OPNsenseItem
from dataclasses import dataclass
import logging

log = logging.getLogger(__name__)


@dataclass
class VXLANInterface(OPNsenseItem):
    description: str
    enabled: bool


class VXLANController(OPNsenseItemController[VXLANInterface]):

    def __init__(self, device):
        super().__init__(device, "interface", "vxlan_settings")

    def _parse_api_response(self, api_response) -> VXLANInterface:
        pass

    def add(self, interface: VXLANInterface) -> VXLANInterface:
        pass

    def set(self, interface: VXLANInterface) -> VXLANInterface:
        pass
