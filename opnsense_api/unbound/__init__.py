from .alias_controller import Alias
from .host_controller import Host
from .domain_controller import Domain


class Unbound(object):

  def __init__(self, device):
    self._device = device

  @property
  def alias_controller(self) -> Alias:
    return Alias(self._device)

  @property
  def host_controller(self) -> Host:
    return Host(self._device)

  @property
  def domain_controller(self) -> Domain:
    return Domain(self._device)
