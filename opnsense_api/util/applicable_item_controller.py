from abc import ABC
from enum import Enum

from opnsense_api.util.exceptions import FailedToApplyChangesException
from opnsense_api.util.item_controller import OPNsenseItemController, T


class OPNsenseApplicableItemController(OPNsenseItemController[T], ABC):
    """
    Controller for OPNSense items that have an apply action.
    """

    class _ItemActions(Enum):
        search = "searchItem"
        get = "getItem"
        add = "addItem"
        set = "setItem"
        delete = "delItem"
        apply = "reconfigure"

    def add(self, controller_item: T) -> None:
        super().add(controller_item)
        self.apply_changes()

    def set(self, controller_item: T) -> None:
        super().set(controller_item)
        self.apply_changes()

    def delete(self, controller_item: T) -> None:
        super().delete(controller_item)
        self.apply_changes()

    def apply_changes(self) -> None:
        """
        Applies pending changes to controller items.

        Note: ``apply_changes`` is automatically called after ``add``, ``set``, and ``delete``.

        """
        response = self._api_post(self._ItemActions.apply.value)
        if response["status"] != "ok":
            raise FailedToApplyChangesException(f"Failed to apply changes. Reason {response}")
