from .loopback_controller import LoopbackController
from .vip_controller import VIPController
from .vlan_controller import VLANController
from .vxlan_controller import VXLANController


class Interfaces(object):

    def __init__(self, device):
        self._device = device

    @property
    def loopback_controller(self) -> LoopbackController:
        return LoopbackController(self._device)

    @property
    def vip_controller(self) -> VIPController:
        return VIPController(self._device)

    @property
    def vlan_controller(self) -> VLANController:
        return VLANController(self._device)

    @property
    def vxlan_controller(self) -> VXLANController:
        return VXLANController(self._device)
