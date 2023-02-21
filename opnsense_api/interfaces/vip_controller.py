from ..util.item_controller import OPNsenseItemController, OPNsenseItem
from dataclasses import dataclass
import logging

log = logging.getLogger(__name__)


@dataclass
class VIPInterface(OPNsenseItem):
    description: str
    interface: str
    mode: str
    descr: str
    subnet: str
    subnet_bits: str
    vhid: str
    advbase: str
    advskew: str
    address: str
    vhid_txt: str


class VIPController(OPNsenseItemController[VIPInterface]):

    def __init__(self, device):
        super().__init__(device, "interfaces", "vip_settings")

    def _parse_api_response(self, api_response) -> VIPInterface:
        return VIPInterface(
        uuid=api_response["uuid"],
        description=api_response["descr"],
        interface=api_response["interface"],
        mode=api_response["mode"],
        descr=api_response["descr"], # TODO: Either remove this one or description
        subnet=api_response["subnet"],
        subnet_bits=api_response["subnet_bits"],
        vhid=api_response["vhid"],
        advbase=api_response["advbase"],
        advskew=api_response["advskew"],
        address=api_response["address"],
        vhid_txt=api_response["vhid_txt"]
        )

    def add(self, interface: VIPInterface) -> VIPInterface:
        pass

    def set(self, interface: VIPInterface) -> VIPInterface:
        pass
