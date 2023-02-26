from abc import ABC
from enum import Enum

from opnsense_api.util.exceptions import FailedToApplyChangesException
from opnsense_api.util.item_controller import OPNsenseItemController, TOPNSenseItem


class OPNsenseApplicableItemController(OPNsenseItemController[TOPNSenseItem], ABC):
    """
    Controller for OPNSense items that have an apply action.
    """

    class ItemActions(Enum):
        search = "searchItem"
        get = "getItem"
        add = "addItem"
        set = "setItem"
        delete = "delItem"
        apply = "reconfigure"

    def add(self, item: TOPNSenseItem) -> None:
        super().add(item)
        self.apply_changes()

    def set(self, item: TOPNSenseItem) -> None:
        super().set(item)
        self.apply_changes()

    def delete(self, item: TOPNSenseItem) -> None:
        super().delete(item)
        self.apply_changes()

    def apply_changes(self) -> None:
        """
        Apply any pending changes

        """
        response = self._api_post(self.ItemActions.apply.value)
        if response["status"] != "ok":
            raise FailedToApplyChangesException(f"Failed to apply changes. Reason {response}")
