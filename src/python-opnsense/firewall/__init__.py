from .. import Opnsense
from alias_controller import Alias

class Firewall(object):

  def __init__(self, device: Opnsense):
    self._device = device

  @property
  def alias_controller(self) -> Alias:
    return Alias(self._device)
