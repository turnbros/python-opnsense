from ..util.item_controller import OPNsenseItemController, OPNsenseItem
from dataclasses import dataclass
from enum import Enum
import logging

log = logging.getLogger(__name__)


@dataclass
class Route(OPNsenseItem):
    # NetworkField{}
    network: str
    # JsonKeyValueStoreField
    gateway: str
    # TextField
    description: str
    # BooleanField
    enabled: bool


class RouteController(OPNsenseItemController[Route]):

    def __init__(self, device):
        super().__init__(device, "routes", "routes")

    class ItemActions(Enum):
        search = "searchroute"
        get = "getroute"
        add = "addroute"
        set = "setroute"
        delete = "delroute"

    def _parse_api_response(self, api_response) -> Route:
        """

        :param api_response:
        :return:
        """

        return Route(
        uuid=api_response["uuid"],
        network=api_response["network"],
        gateway=api_response["gateway"],
        description=api_response["descr"],
        enabled=bool(api_response["disabled"])
        )

    def add(self, route: Route) -> Route:
        pass

    def set(self, route: Route) -> Route:
        pass
