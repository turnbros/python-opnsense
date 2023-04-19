from abc import ABC

from opnsense_api.unbound.service_controller import UnboundServiceController
from opnsense_api.util.applicable_item_controller import OPNsenseApplicableItemController
from opnsense_api.util.item_controller import T


class UnboundResourceController(OPNsenseApplicableItemController[T], ABC):
    """
    Unbound Controllers extend this, so changes get applied at api/unbound/service/reconfigure.
    """

    _unbound_service_controller: UnboundServiceController

    def __init__(self, device):
        super().__init__(device=device, module="unbound", controller="settings")
        self._unbound_service_controller = UnboundServiceController(device)

    def apply_changes(self) -> None:
        self._unbound_service_controller.apply_changes()
