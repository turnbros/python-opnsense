import logging
from typing import TypeVar, Generic, List
from opnsense_api.unbound.util import format_request, parse_unbound_resource, BaseOverride

log = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseOverride)


class UnboundResource(Generic[T]):

  def __init__(self, device, resource_type):
    self._device = device
    self._module = "unbound"
    self._controller = "settings"
    self._resource_type = resource_type
    self._functions = {
        "host": {
            "search": "searchHostOverride",
            "get": "getHostOverride",
            "add": "addHostOverride",
            "toggle": "toggleHostOverride",
            "delete": "delHostOverride",
            "set": "setHostOverride"
        },
        "domain": {
            "search": "searchDomainOverride",
            "get": "getDomainOverride",
            "add": "addDomainOverride",
            "toggle": "toggleDomainOverride",
            "delete": "delDomainOverride",
            "set": "setDomainOverride"
        },
        "alias": {
            "search": "searchHostAlias",
            "get": "getHostAlias",
            "add": "addHostAlias",
            "toggle": "toggleHostAlias",
            "delete": "delHostAlias",
            "set": "setHostAlias"
        }
    }

  def _get_function_name(self, function: str):
    return self._functions[self._resource_type][function]

  def apply_changes(self) -> None:
    """
    Apply any pending Unbound changes

    """
    response = self._device._authenticated_request("POST", f"unbound/service/reconfigure")
    if response["status"] != "ok":
      raise Exception(f"Failed to apply changes. Reason {response}")

  def match_by_attributes(self, **kwargs) -> List[T]:
    """
    Matches and returns Unbound overrides. The match is based on attribute values provided as kwargs.

    :param kwargs: { "description": "a filter rule description", "log": True }
    :return: A list of matched overrides
    :rtype List[T]:
    """
    all_items = self.list()
    matched_items = []
    for item in all_items:
      item_uuid = item.get("uuid")
      print(item_uuid)

      item_match = self.get(item_uuid)
      print(item_match)

      item_match.uuid = item_uuid
      item_matched = True
      for key in kwargs.keys():
        if item_match.get(key) != kwargs.get(key):
          item_matched = False
          break
      if item_matched:
        matched_items.append(item_match)

    return matched_items

  def list(self) -> List[T]:
    """
    Returns a list of the configured Unbound overrides.

    :return: A list of Unbound overrides
    :rtype List[T]:
    """
    request_base = format_request(self._module, self._controller, self._get_function_name("search"))
    search_results = self._device._authenticated_request("GET", request_base)
    if 'rows' in search_results:
      return search_results['rows']
    return []

  def get(self, uuid: str) -> T:
    """
    Retrieves an Unbound override by UUID. If the override isn't found an exception will be raised.

    :param uuid: The UUID of the override to retrieve
    :return: The Unbound override
    :rtype T:
    """
    request_base = format_request(self._module, self._controller, self._get_function_name("get"), uuid)
    query_response = self._device._authenticated_request("GET", request_base)
    if self._resource_type in query_response:
      try:
        return parse_unbound_resource(self._resource_type, uuid, query_response[self._resource_type])
      except Exception as error:
        raise Exception(f"Failed to parse the {self._resource_type} overrides with UUID: {uuid}\nException: {error.with_traceback()}")

    raise Exception(f"A DomainOverride with the UUID {uuid} was not found!")

  def delete(self, uuid: str) -> None:
    """
    Delete an Unbound override.

    :param uuid: The UUID of the override to delete
    :rtype None:
    """
    request_base = format_request(self._module, self._controller, self._get_function_name("delete"), uuid)
    response = self._device._authenticated_request("POST", request_base)
    if response['result'] != "deleted":
      raise Exception(f"Failed to delete host override with UUID {uuid} with reason: {response['result']}")
    self.apply_changes()

  def toggle(self, uuid: str, enabled=None) -> T:
    """
    Toggle an Unbound override using just the UUID, or set the enabled state through the enabled parameter.

    :param uuid: The UUID of the override to toggle.
    :param enabled: Set `enabled` to override the default toggle behaviour.
    :return: The unbound object that was just toggled.
    :rtype T:
    """
    if enabled is None:
      enabled = bool(int(self.get(uuid).enabled))
    request_base = format_request(self._module, self._controller, self._get_function_name("toggle"), uuid, {"enabled": not enabled})
    response = self._device._authenticated_request("POST", request_base)
    if response["changed"]:
      self.apply_changes()
      return self.get(uuid)
