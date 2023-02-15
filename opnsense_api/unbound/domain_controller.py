import logging
from .controller import UnboundResource
from .util import format_request, DomainOverride

log = logging.getLogger(__name__)


class Domain(UnboundResource[DomainOverride]):

  def __init__(self, device):
    super().__init__(device, "domain")

  def add(self,
          domain: str,
          server: str,
          description: str = "",
          enabled: bool = True,
          ) -> DomainOverride:
    """

    :param domain:
    :param server:
    :param description:
    :param enabled:
    :return: DomainOverride
    """
    request_body = {
      "domain": {
        "domain": domain,
        "server": server,
        "description": description,
        "enabled": str(int(enabled))
      }
    }
    # TODO: Handle the fact that a failure still results in HTTP 200
    request_base = format_request(self._module, self._controller, "addDomainOverride")
    response = self._device._authenticated_request("POST", request_base, body=request_body)
    if response['result'] == "saved":
      self.apply_changes()
      return self.get(response['uuid'])
    else:
      raise Exception(f"Failed to add domain override. Reason: {response}")

  def set(self,
          uuid: str,
          domain: str,
          server: str,
          description: str = "",
          enabled: bool = True,
          ) -> DomainOverride:
    """

    :param uuid:
    :param domain:
    :param server:
    :param description:
    :param enabled:
    :return: DomainOverride
    """
    request_body = {
      "domain": {
        "domain": domain,
        "server": server,
        "description": description,
        "enabled": str(int(enabled))
      }
    }
    request_base = format_request(self._module, self._controller, "setDomainOverride", uuid)

    response = self._device._authenticated_request("POST", request_base, body=request_body)
    if response['result'] == "saved":
      self.apply_changes()
      return self.get(uuid)
    else:
      raise Exception(f"Failed to update domain override. Reason: {response}")
