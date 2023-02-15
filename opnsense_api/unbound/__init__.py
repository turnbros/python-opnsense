from .alias_controller import Alias
from .host_controller import Host
from .domain_controller import Domain


class Unbound(object):

  def __init__(self, device):
    self._device = device

  @property
  def host_alias_controller(self) -> Alias:
    return Alias(self._device)

  @property
  def host_override_controller(self) -> Host:
    return Host(self._device)

  @property
  def domain_override_controller(self) -> Domain:
    return Domain(self._device)

  def apply_changes(self):
    response = self._device._authenticated_request("GET", f"unbound/service/reconfigure")
    if response["status"] != "ok":
      raise Exception(f"Failed to apply changes. Reason {response}")


