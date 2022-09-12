from typing import List, Union

from .util import format_request, parse_unbound_host_override, apply_changes, HostOverride


class Host(object):

  def __init__(self, device):
    self._device = device
    self._module = "unbound"
    self._controller = "settings"

  def list(self) -> List[HostOverride]:
    """

    :return: List[HostOverride]
    """
    request_base = format_request(self._module, self._controller, "searchHostOverride")
    search_results = self._device._authenticated_request("GET", request_base)
    if 'rows' in search_results:
      return search_results['rows']
    return []

  def get(self, uuid: str) -> Union[HostOverride, None]:
    """

    :param uuid:
    :return: HostOverride"
    """
    request_base = format_request(self._module, self._controller, "getHostOverride", uuid)
    query_response = self._device._authenticated_request("GET", request_base)
    if 'host' in query_response:
      try:
        return parse_unbound_host_override(uuid, query_response['host'])
      except Exception as error:
        raise Exception(f"Failed to parse the host overrides with UUID: {uuid}\nException: {error.with_traceback()}")
    return None

  def toggle(self, uuid: str, enabled=None) -> HostOverride:
    """

    :param uuid:
    :param enabled:
    :return: HostOverride
    """
    if enabled is None:
      enabled = bool(int(self.get(uuid)['enabled']))
    request_base = format_request(self._module, self._controller, 'toggleHostOverride', uuid, {"enabled": not enabled})
    response = self._device._authenticated_request("POST", request_base)
    if response["changed"]:
      apply_changes(self._device)
      return self.get(uuid)

  def delete(self, uuid: str) -> bool:
    """

    :param uuid:
    :return: bool
    """
    request_base = format_request(self._module, self._controller, "delHostOverride", uuid)
    response = self._device._authenticated_request("POST", request_base)
    if response['result'] == "deleted":
      apply_changes(self._device)
      return True
    raise Exception(f"Failed to delete host override with UUID {uuid} with reason: {response['result']}")

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
      apply_changes(self._device)
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
      apply_changes(self._device)
      return self.get(uuid)
    else:
      raise Exception(f"Failed to update host override. Reason: {response}")
