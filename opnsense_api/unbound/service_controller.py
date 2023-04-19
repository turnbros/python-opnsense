from enum import Enum

from opnsense_api.util.controller import OPNsenseAPIController
from opnsense_api.util.exceptions import FailedToApplyChangesException, FailedToRestartException


# TODO: Move to generalized class like item controller
class UnboundServiceController(OPNsenseAPIController):
    class _ItemActions(Enum):
        apply = "reconfigure"
        restart = "restart"
        start = "start"
        status = "status"
        stop = "stop"

    def __init__(self, device):
        super().__init__(device, "unbound", "service")

    def apply_changes(self) -> None:
        """
        Apply any pending changes to the service.

        """
        response = self._api_post(self._ItemActions.apply.value)
        if response["status"] != "ok":
            raise FailedToApplyChangesException(f"Failed to apply changes. Reason {response}")

    def restart(self) -> None:
        """
        Restarts the Unbound service

        """
        response = self._api_post(self._ItemActions.restart.value)
        if response["response"] != "OK":
            raise FailedToRestartException(f"Failed to apply changes. Reason {response}")

    def start(self) -> None:
        """
        Starts the Unbound service

        """
        response = self._api_post(self._ItemActions.start.value)
        if response["response"] != "OK":
            raise FailedToRestartException(f"Failed to apply changes. Reason {response}")

    def status(self) -> str:
        """
        Returns the status of the Unbound service

        """
        response = self._api_get(self._ItemActions.status.value)
        return response["status"]

    def stop(self) -> None:
        """
        Stops the Unbound service

        """
        response = self._api_post(self._ItemActions.stop.value)
        if response["response"] != "OK":
            raise FailedToRestartException(f"Failed to apply changes. Reason {response}")
