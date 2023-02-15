import logging
from .controller import UnboundResource
from .util import format_request, HostAlias

log = logging.getLogger(__name__)


class Alias(UnboundResource[HostAlias]):

  def __init__(self, device):
    super().__init__(device, "alias")

  def add(self,
          name: str,
          domain: str,
          host_uuid: str,
          description: str = "",
          enabled: bool = True,
          ) -> HostAlias:
    """
    Adds a new alias to an existing host.

    :param name: The name of the alias. In the UI this is the `host` field.
    :param domain: A domain for the alias.
    :param host_uuid: The UUID of the host this alias will be associated with.
    :param description: A description for this host alias.
    :param enabled: Whether the alias is enabled.
    :return: HostAlias
    """
    request_body = {
      "alias": {
        "hostname": name,
        "domain": domain,
        "host": host_uuid,
        "description": description,
        "enabled": str(int(enabled))
      }
    }
    request_base = format_request(self._module, self._controller, "addHostAlias")
    response = self._device._authenticated_request("POST", request_base, body=request_body)
    if response['result'] == "saved":
      self.apply_changes()
      return self.get(response['uuid'])
    else:
      raise Exception(f"Failed to add host alias. Reason: {response}")

  def set(self,
          uuid: str,
          name: str,
          domain: str,
          host_uuid: str,
          description: str = "",
          enabled: bool = True,
          ) -> HostAlias:
    """
    Updates an existing HostAlias.

    :param uuid: The UUID of the alias. This is generated when the alias is created.
    :param name: The name of the alias. In the UI this is the `host` field.
    :param domain: A domain for the alias.
    :param host_uuid: The UUID of the host this alias will be associated with.
    :param description: A description for this host alias.
    :param enabled: Whether the alias is enabled.
    :return: HostAlias
    """
    request_body = {
      "alias": {
        "hostname": name,
        "domain": domain,
        "host": host_uuid,
        "description": description,
        "enabled": str(int(enabled))
      }
    }
    request_base = format_request(self._module, self._controller, "setHostAlias", uuid)
    response = self._device._authenticated_request("POST", request_base, body=request_body)
    if response['result'] == "saved":
      self.apply_changes()
      return self.get(uuid)
    else:
      raise Exception(f"Failed to update host alias. Reason: {response}")
