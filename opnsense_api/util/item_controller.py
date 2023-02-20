import json
from dataclasses import dataclass, fields, asdict
from .controller import OPNsenseAPIController
from typing import List, TypeVar, Generic
from abc import abstractmethod
from enum import Enum
import logging

log = logging.getLogger(__name__)
T = TypeVar('T', bound='OPNsenseItem')


@dataclass
class OPNsenseItem:
  # Maybe we could extend pydantic.BaseModel here

  uuid: str

  def to_dict(self):
    opnsense_item = asdict(self)
    opnsense_item_dict = {}
    for field in fields(self):
      opnsense_item_dict[field.metadata.get("json_name", field.name)] = opnsense_item.get(field.name)

    return opnsense_item_dict

  def to_json(self):
    return json.dumps(self.to_dict())


class OPNsenseItemController(Generic[T], OPNsenseAPIController):

  # This gets overridden if the controller uses different action verbs
  # See Routes: https://docs.opnsense.org/development/api/core/routes.html
  class ItemActions(Enum):
    search = "searchItem"
    get = "getItem"
    add = "addItem"
    set = "setItem"
    delete = "delItem"
    apply = "reconfigure"

  def list(self) -> List[T]:
    """
    Returns a list of items.

    :return: A list of OPNsense items
    :rtype List[T]:
    """
    items = []
    search_results = self._api_get(self.ItemActions.search.value)
    if 'rows' in search_results:
      for item in search_results['rows']:
        items.append(self._parse_api_response(item))

    return items

  def get(self, uuid) -> T:
    """
    Gets a specific item

    :param uuid:
    :return: T
    """
    result = self._api_get(self.ItemActions.get.value, uuid)
    item = list(result.values())[0]
    return self._parse_api_response(item)

  def delete(self, item: T) -> None:
    """
    Deletes the item

    :param item:
    :return:
    """
    response = self._api_post(self.ItemActions.delete.value, item.uuid)
    if response['result'] != "deleted":
      raise Exception(f"Failed to delete host override with UUID {item.uuid} with reason: {response['result']}")
    self.apply_changes()

  def apply_changes(self) -> None:
    """
    Apply any pending changes

    """
    response = self._api_post(self.ItemActions.apply.value)
    if response["status"] != "ok":
      raise Exception(f"Failed to apply changes. Reason {response}")

  @abstractmethod
  def _parse_api_response(self, api_response) -> T:
    raise NotImplementedError("This method needs to be implemented!")

  @abstractmethod
  def add(self, item: T) -> T:
    raise NotImplementedError("This method needs to be implemented!")

  @abstractmethod
  def set(self, item: T) -> T:
    raise NotImplementedError("This method needs to be implemented!")
