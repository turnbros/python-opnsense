from typing import List, Union

from .util import format_request, parse_unbound_host_alias, apply_changes, HostAlias


class Alias(object):

  def __init__(self, device):
    self._device = device
    self._module = "unbound"
    self._controller = "settings"

  def list(self) -> List[HostAlias]:
    """

    :return: List[HostAlias]
    """
    request_base = format_request(self._module, self._controller, "searchHostAlias")
    response = self._device._authenticated_request("GET", request_base)
    if 'rows' in response:
      return response['rows']
    return []

  def get(self, uuid: str) -> Union[HostAlias, None]:
    """

    :param uuid:
    :return: HostAlias
    """
    request_base = format_request(self._module, self._controller, "getHostAlias", uuid)
    response = self._device._authenticated_request("GET", request_base)
    if 'alias' in response:
      try:
        return parse_unbound_host_alias(uuid, response['alias'])
      except Exception as error:
        raise Exception(f"Failed to parse the alias with UUID: {uuid}\nException: {error.with_traceback()}")
    return None

  def toggle(self, uuid: str, enabled=None) -> HostAlias:
    """

    :param uuid:
    :param enabled:
    :return: HostAlias
    """
    if enabled is None:
      enabled = bool(int(self.get(uuid)['enabled']))
    request_base = format_request(self._module, self._controller, "toggleHostAlias", uuid, {enabled: not enabled})
    response = self._device._authenticated_request("POST", request_base)
    if response["changed"]:
      apply_changes(self._device)
      return self.get(uuid)

  def delete(self, uuid: str) -> bool:
    """

    :param uuid:
    :return: bool
    """
    request_base = format_request(self._module, self._controller, "delHostAlias", uuid)
    response = self._device._authenticated_request("POST", request_base)
    if response['result'] == "deleted":
      apply_changes(self._device)
      return True
    raise Exception(f"Failed to delete host alias with UUID {uuid} with reason: {response['result']}")

  def add(self,
          name: str,
          domain: str,
          host_uuid: str,
          description: str = "",
          enabled: bool = True,
          ) -> HostAlias:
    """

    :param name:
    :param domain:
    :param host_uuid:
    :param description:
    :param enabled:
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
      apply_changes(self._device)
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

    :param uuid:
    :param name:
    :param domain:
    :param host_uuid:
    :param description:
    :param enabled:
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
      apply_changes(self._device)
      return self.get(uuid)
    else:
      raise Exception(f"Failed to update host alias. Reason: {response}")
