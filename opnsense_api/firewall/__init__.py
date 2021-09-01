from .alias_controller import Alias

class Firewall(object):

  def __init__(self, device):
    self._device = device

  @property
  def alias_controller(self) -> Alias:
    return Alias(self._device)
