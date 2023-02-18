from .loopback_controller import LoopbackController as Loopback
from .vip_controller import VIPController as VIP
from .vlan_controller import VLANController as VLAN
from .vxlan_controller import VXLANController as VXLAN


class Interfaces(object):

  def __init__(self, device):
    self._device = device

  @property
  def loopback_controller(self) -> Loopback:
    return Loopback(self._device)

  @property
  def vip_controller(self) -> VIP:
    return VIP(self._device)

  @property
  def vlan_controller(self) -> VLAN:
    return VLAN(self._device)

  @property
  def vxlan_controller(self) -> VXLAN:
    return VXLAN(self._device)
