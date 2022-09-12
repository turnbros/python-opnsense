from typing import List, Union

from .util import format_request, parse_unbound_domain_override, apply_changes, DomainOverride


class Domain(object):

  def __init__(self, device):
    self._device = device
    self._module = "unbound"
    self._controller = "settings"

  def list(self) -> List[DomainOverride]:
    """

    :return: List[DomainOverride]
    """
    request_base = format_request(self._module, self._controller, "searchDomainOverride")
    search_results = self._device._authenticated_request("GET", request_base)
    if 'rows' in search_results:
      return search_results['rows']
    return []

  def get(self, uuid: str) -> Union[DomainOverride, None]:
    """

    :param uuid:
    :return: DomainOverride
    """
    request_base = format_request(self._module, self._controller, "getDomainOverride", uuid)
    response = self._device._authenticated_request("GET", request_base)
    if 'domain' in response:
      try:
        return parse_unbound_domain_override(uuid, response['domain'])
      except Exception as error:
        raise Exception(f"Failed to parse the domain override with UUID: {uuid}\nException: {error.with_traceback()}")
    return None

  def toggle(self, uuid: str, enabled=None) -> DomainOverride:
    """

    :param uuid:
    :param enabled:
    :return: DomainOverride
    """
    if enabled is None:
      enabled = bool(int(self.get(uuid)['enabled']))
    request_base = format_request(self._module, self._controller, 'toggleDomainOverride', uuid, {enabled: not enabled})
    response = self._device._authenticated_request("POST", request_base)
    if response["changed"]:
      apply_changes(self._device)
      return self.get(uuid)

  def delete(self, uuid: str) -> bool:
    """

    :param uuid:
    :return: bool
    """
    request_base = format_request(self._module, self._controller, "delDomainOverride", uuid)
    response = self._device._authenticated_request("POST", request_base)
    if response['result'] == "deleted":
      apply_changes(self._device)
      return True
    raise Exception(f"Failed to delete domain override with UUID {uuid} with reason: {response['result']}")

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
      apply_changes(self._device)
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
      apply_changes(self._device)
      return self.get(response['uuid'])
    else:
      raise Exception(f"Failed to update domain override. Reason: {response}")