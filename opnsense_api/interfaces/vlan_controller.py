from ..util.item_controller import OPNsenseItemController, OPNsenseItem
from dataclasses import dataclass
import logging

log = logging.getLogger(__name__)


@dataclass
class VLANInterface(OPNsenseItem):
    description: str
    enabled: bool


class VLANController(OPNsenseItemController[VLANInterface]):

    def __init__(self, device):
        super().__init__(device, "interface", "vlan_settings")

    def _parse_api_response(self, api_response) -> VLANInterface:
        pass

    def add(self, interface: VLANInterface) -> VLANInterface:
        pass

    def set(self, interface: VLANInterface) -> VLANInterface:
        pass
