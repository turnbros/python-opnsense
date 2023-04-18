import logging
from enum import Enum

from pydantic import constr, Field

from ..util.applicable_item_controller import OPNsenseApplicableItemController
from ..util.item_controller import OPNsenseItem
from ..util.parse import parse_selected_keys

log = logging.getLogger(__name__)


class Route(OPNsenseItem):
    disabled: bool = True
    network: str
    gateway: constr(regex=r"^[a-zA-Z0-9_]*$")
    description: str = Field(default="", alias="descr")

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return Route(
            uuid=uuid,
            disabled=bool(int(api_response["disabled"])),
            network=api_response["network"],
            gateway=parse_selected_keys(api_response["gateway"])[0],
            descr=api_response["descr"]
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        return Route(
            uuid=api_response["uuid"],
            disabled=bool(int(api_response["disabled"])),
            network=api_response["network"],
            gateway=api_response["gateway"].split(' ')[0],
            descr=api_response["descr"]
        )


class RouteController(OPNsenseApplicableItemController[Route]):

    def __init__(self, device):
        super().__init__(device, "routes", "routes")

    @property
    def opnsense_item_class(self) -> type[Route]:
        return Route

    class _ItemActions(Enum):
        search = "searchroute"
        get = "getroute"
        add = "addroute"
        set = "setroute"
        delete = "delroute"
        apply = "reconfigure"
