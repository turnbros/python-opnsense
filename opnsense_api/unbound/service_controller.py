from enum import Enum

from opnsense_api.util.controller import OPNsenseAPIController
from opnsense_api.util.exceptions import FailedToApplyChangesException, FailedToRestartException


# TODO: Move to generalized class like item controller
class UnboundServiceController(OPNsenseAPIController):
    class ItemActions(Enum):
        apply = "reconfigure"
        restart = "restart"
        start = "start"
        status = "status"
        stop = "stop"

    def __init__(self, device):
        super().__init__(device, "unbound", "service")

    def apply_changes(self) -> None:
        response = self._api_post(self.ItemActions.apply.value)
        if response["status"] != "ok":
            raise FailedToApplyChangesException(f"Failed to apply changes. Reason {response}")

    def restart(self) -> None:
        response = self._api_post(self.ItemActions.restart.value)
        if response["response"] != "OK":
            raise FailedToRestartException(f"Failed to apply changes. Reason {response}")

    def start(self) -> None:
        response = self._api_post(self.ItemActions.start.value)
        if response["response"] != "OK":
            raise FailedToRestartException(f"Failed to apply changes. Reason {response}")

    def status(self) -> str:
        response = self._api_get(self.ItemActions.status.value)
        return response["status"]

    def stop(self) -> None:
        response = self._api_post(self.ItemActions.stop.value)
        if response["response"] != "OK":
            raise FailedToRestartException(f"Failed to apply changes. Reason {response}")
