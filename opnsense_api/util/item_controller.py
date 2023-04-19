from __future__ import annotations

from abc import abstractmethod, ABC
from enum import Enum
from typing import List, TypeVar, Generic, Optional

from pydantic import BaseModel

from .controller import OPNsenseAPIController
from .exceptions import FailedToDeleteException, ItemNotFoundException, FailedToSetItemException, \
    FailedToAddItemException, InvalidItemException


class OPNsenseItem(BaseModel, ABC):
    class Config:
        """
        Config class that:
          - ensures validation of all fields, whenever a field is set directly.
          - allows populating of fields via alias
        """
        validate_assignment = True
        allow_population_by_field_name = True

    uuid: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        """
        Parses the Item from the API response to getItem

        :param api_response: API response to getItem
        :param uuid: the UUID that was originally searched for, as it's often not part of the response
        :return: Item from API response
        """
        return cls.parse_obj({"uuid": uuid} | api_response)

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        """
        Parses the Item from the API response to list

        :param api_response: API response to list
        :return: Item from API response
        """
        return cls.parse_obj(api_response)

    def _get_api_name(self):
        return type(self).__name__.lower()

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

    def _get_api_representation(self) -> dict:
        """
        Returns an OPNsenseItems dictionary representation as the OPNSense API understands it when setting or adding.

        """
        return {
            self._get_api_name():
                self.__replace_ints_with_strings(
                    self.__replace_booleans_with_numbers(
                        self.__replace_lists(
                            self.__replace_enums_with_values(
                                self.dict(by_alias=True, exclude_none=True)
                            )
                        )
                    )
                )
        }


T = TypeVar('T', bound=OPNsenseItem)


class OPNsenseItemController(Generic[T], OPNsenseAPIController, ABC):

    # This gets overridden if the controller uses different action verbs
    # See Routes: https://docs.opnsense.org/development/api/core/routes.html
    class _ItemActions(Enum):
        search = "searchItem"
        get = "getItem"
        add = "addItem"
        set = "setItem"
        delete = "delItem"
        # toggle = "toggleItem"
        # removed toggle, we should just use set

    @property
    @abstractmethod
    def _opnsense_item_class(self) -> type[T]:
        raise NotImplementedError("Not implemented!")

    @abstractmethod
    def __init__(self, device, module: str, controller: str):
        super().__init__(device, module, controller)

    def list(self) -> List[T]:
        """
        Returns a list of OPNsenseItems that exist on an OPNsense device.

        """
        query_response = self._api_post(self._ItemActions.search.value)
        return [self._opnsense_item_class._from_api_response_list(item) for item in query_response.get('rows')]  # type: ignore

    def get(self, uuid: str) -> T:
        """
        Gets a specific OPNsenseItem by UUID from an OPNsense device

        """
        query_response = self._api_get(self._ItemActions.get.value, uuid)
        if len(query_response.values()) != 1:
            raise ItemNotFoundException(self._opnsense_item_class.__name__, uuid, query_response)
        return self._opnsense_item_class._from_api_response_get(list(query_response.values())[0], uuid=uuid)  # type: ignore

    def delete(self, controller_item: T) -> None:
        """
        Deletes the supplied item from an OPNsense device

        """
        query_response = self._api_post(self._ItemActions.delete.value, controller_item.uuid)
        if query_response['result'] != "deleted":
            raise FailedToDeleteException(self._opnsense_item_class.__name__, controller_item.uuid, query_response)

    def add(self, controller_item: T) -> None:
        """
        Adds an OPNsenseItem object without a UUID to an OPNsense device then updates the input OPNsenseItem objects UUID

        """
        query_response = self._api_post(self._ItemActions.add.value,
                                        body=controller_item._get_api_representation())
        if query_response['result'] != "saved":
            raise FailedToAddItemException(self._opnsense_item_class.__name__, controller_item.uuid, query_response)
        controller_item.uuid = query_response['uuid']

    def set(self, controller_item: T) -> None:
        """
        Updates an OPNsenseItem on an OPNsense device

        """
        # get the item first to ensure it exists
        if not controller_item.uuid:
            raise InvalidItemException(self._opnsense_item_class.__name__,
                                       custom_message="Can't set item without knowing it's UUID.")
        self.get(controller_item.uuid)

        query_response = self._api_post(self._ItemActions.set.value, controller_item.uuid,
                                        body=controller_item._get_api_representation())
        if query_response['result'] != "saved":
            raise FailedToSetItemException(self._opnsense_item_class.__name__, controller_item.uuid, query_response)
