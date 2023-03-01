from __future__ import annotations

from abc import abstractmethod, ABC
from enum import Enum
from typing import List, TypeVar, Generic, Union

from pydantic import BaseModel

from .controller import OPNsenseAPIController
from .exceptions import FailedToDeleteException, ItemNotFoundException, FailedToSetItemException, \
    FailedToAddItemException, InvalidItemException

TOPNSenseItem = TypeVar('TOPNSenseItem', bound='OPNSenseItem')


class OPNsenseItem(BaseModel, ABC):
    class Config:
        """
        Config class that:
          - ensures validation of all fields, whenever a field is set directly.
          - allows populating of fields via alias
        """
        validate_assignment = True
        allow_population_by_field_name = True

    uuid: Union[str, None]

    # So my IDE stops screaming at me about unexpected arguments whenever I want to instantiate a subclass with more
    # than just uuid.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    @abstractmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        """
        Parses the Item from the API response to getItem
        :param api_response: API response to getItem
        :param uuid: the UUID that was originally searched for, as it's often not part of the response
        :return: Item from API response
        """
        raise NotImplementedError("This method needs to be implemented!")

    @classmethod
    @abstractmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        """
        Parses the Item from the API response to list
        :param api_response: API response to list
        :return: Item from API response
        """
        raise NotImplementedError("This method needs to be implemented!")

    def _get_api_name(self):
        return type(self).__name__.lower()

    @staticmethod
    def __strip_none_fields(dictionary: dict) -> dict:
        return {k: v for k, v in dictionary.items() if v is not None}

    @staticmethod
    def __replace_booleans_with_numbers(dictionary: dict):
        for k, v in dictionary.items():
            if isinstance(v, bool):
                dictionary[k] = "1" if v else "0"
        return dictionary

    @staticmethod
    def __replace_ints_with_strings(dictionary: dict):
        return {k: str(v) if isinstance(v, int) else v for k, v in dictionary.items()}

    @staticmethod
    def __replace_lists(dictionary: dict):
        return {k: str.join('\n', v) if isinstance(v, list) else v for k, v in dictionary.items()}

    @staticmethod
    def __replace_enums_with_values(dictionary: dict):
        return {k: v.value if isinstance(v, Enum) else v for k, v in dictionary.items()}

    def get_api_representation(self) -> dict:
        """

        :return: the items dictionary representation as the OPNSense API understands it when setting or adding.
        """
        return {
            self._get_api_name():
                self.__replace_ints_with_strings(
                    self.__replace_booleans_with_numbers(
                        self.__replace_lists(
                            self.__replace_enums_with_values(
                                self.__strip_none_fields(self.dict(by_alias=True))
                            )
                        )
                    )
                )
        }


class OPNsenseItemController(Generic[TOPNSenseItem], OPNsenseAPIController, ABC):
    # This gets overridden if the controller uses different action verbs
    # See Routes: https://docs.opnsense.org/development/api/core/routes.html
    class ItemActions(Enum):
        search = "searchItem"
        get = "getItem"
        add = "addItem"
        set = "setItem"
        delete = "delItem"
        # toggle = "toggleItem"
        # removed toggle, we should just use set

    @property
    @abstractmethod
    def opnsense_item_class(self) -> type[TOPNSenseItem]:
        """
        :return: the class of the implementation of OPNSenseItem this class controls.
        """
        raise NotImplementedError("Not implemented!")

    @abstractmethod
    def __init__(self, device, module: str, controller: str):
        super().__init__(device, module, controller)

    def list(self) -> List[TOPNSenseItem]:
        """
        Returns a list of items.

        :return: A list of OPNsense items
        :rtype List[T]:
        """
        query_response = self._api_post(self.ItemActions.search.value)
        return [self.opnsense_item_class._from_api_response_list(item) for item in query_response.get('rows')]

    def get(self, uuid: str) -> TOPNSenseItem:
        """
        Gets a specific item

        :param uuid:
        :return: T
        """
        query_response = self._api_get(self.ItemActions.get.value, uuid)
        if len(query_response.values()) != 1:
            raise ItemNotFoundException(self.opnsense_item_class.__name__, uuid, query_response)
        return self.opnsense_item_class._from_api_response_get(list(query_response.values())[0], uuid=uuid)

    def delete(self, item: TOPNSenseItem) -> None:
        """
        Deletes the item

        :param item: Item to be deleted
        """
        query_response = self._api_post(self.ItemActions.delete.value, item.uuid)
        if query_response['result'] != "deleted":
            raise FailedToDeleteException(self.opnsense_item_class.__name__, item.uuid, query_response)

    def add(self, item: TOPNSenseItem) -> None:
        """
        Adds the item to the OPNSense and saves the items UUID in the parameter item
        :param item: Will be created on the OPNSense and UUID will be updated after creation
        """
        query_response = self._api_post(self.ItemActions.add.value,
                                        body=item.get_api_representation())
        if query_response['result'] != "saved":
            raise FailedToAddItemException(self.opnsense_item_class.__name__, item.uuid, query_response)
        item.uuid = query_response['uuid']

    def set(self, item: TOPNSenseItem) -> None:
        """
        Updates the items state in the OPNSense

        :param item: state of item to be set on OPNSense
        """
        # get the item first to ensure it exists
        if not item.uuid:
            raise InvalidItemException(self.opnsense_item_class.__name__,
                                       custom_message="Can't set item without knowing it's UUID.")
        self.get(item.uuid)

        query_response = self._api_post(self.ItemActions.set.value, item.uuid,
                                        body=item.get_api_representation())
        if query_response['result'] != "saved":
            raise FailedToSetItemException(self.opnsense_item_class.__name__, item.uuid, query_response)
