import logging
from .controller import UnboundResource
from .util import format_request, HostOverride

log = logging.getLogger(__name__)


class Host(UnboundResource[HostOverride]):

  def __init__(self, device):
    super().__init__(device, "host")

  def add(self,
          name: str,
          domain: str,
          server: str,
          description: str = "",
          enabled: bool = True,
          rr: str = "",
          mxprio: int = 0,
          mx: str = ""
          ) -> HostOverride:
    """
    Adds a new HostOverride.

    :param name: The name of the override. In the UI this is the host field
    :param domain: The overrides domain.
    :param server: The IP address that will be returned for this host and domain
    :param rr: The type of record this overrides
    :param mxprio: MX Record priority
    :param mx: If overriding an MX record, the MX hostname to return
    :param description: The overrides' description.
    :param enabled: Whether the override is enabled.
    :return: HostOverride
    """
    request_body = {
      "host": {
        "hostname": name,
        "domain": domain,
        "server": server,
        "description": description,
        "rr": rr,
        "mxprio": mxprio,
        "mx": mx,
        "enabled": str(int(enabled))
      }
    }
    request_base = format_request(self._module, self._controller, "addHostOverride")
    response = self._device._authenticated_request("POST", request_base, body=request_body)
    if response['result'] == "saved":
      self.apply_changes()
      return self.get(response['uuid'])
    else:
      raise Exception(f"Failed to add host override. Reason: {response}")

  def set(self,
          uuid: str,
          name: str,
          domain: str,
          server: str,
          description: str = "",
          enabled: bool = True,
          rr: str = "",
          mxprio: int = 0,
          mx: str = "",
          ) -> HostOverride:
    """
    Updates an existing HostOverride.

    :param uuid: The UUID of the override. This is generated when the override is created.
    :param name: The name of the override. In the UI this is the host field.
    :param domain: The overrides domain.
    :param server: The IP address that will be returned for this host and domain
    :param rr: The type of record this overrides
    :param mxprio: MX Record priority
    :param mx: If overriding an MX record, the MX hostname to return
    :param description: The overrides' description.
    :param enabled: Whether the override is enabled.
    :return: HostOverride
    """
    request_body = {
      "host": {
        "hostname": name,
        "domain": domain,
        "server": server,
        "description": description,
        "rr": rr,
        "mxprio": mxprio,
        "mx": mx,
        "enabled": str(int(enabled))
      }
    }
    request_base = format_request(self._module, self._controller, "setHostOverride", uuid)
    response = self._device._authenticated_request("POST", request_base, body=request_body)
    if response['result'] == "saved":
      self.apply_changes()
      return self.get(uuid)
    else:
      raise Exception(f"Failed to update host override. Reason: {response}")
