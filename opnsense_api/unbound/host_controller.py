import logging
from .controller import UnboundResource
from .util import format_request, HostOverride

log = logging.getLogger(__name__)


class Host(UnboundResource):

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

    :param name:
    :param domain:
    :param server:
    :param rr:
    :param mxprio:
    :param mx:
    :param description:
    :param enabled:
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

    :param uuid:
    :param name:
    :param domain:
    :param server:
    :param rr:
    :param mxprio:
    :param mx:
    :param description:
    :param enabled:
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
