from enum import Enum

from opnsense_api.unbound.resource_controller import UnboundResourceController
from opnsense_api.util.item_controller import OPNsenseItem


class DomainOverride(OPNsenseItem):
    enabled: bool = True
    domain: str
    server: str
    description: str = ""

    def _get_api_name(self):
        return "domain"

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return DomainOverride.parse_obj(api_response | {"uuid": uuid})

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        return DomainOverride.parse_obj(api_response)


class DomainController(UnboundResourceController[DomainOverride]):
    class _ItemActions(Enum):
        search = "searchDomainOverride"
        get = "getDomainOverride"
        add = "addDomainOverride"
        set = "setDomainOverride"
        delete = "delDomainOverride"
        apply = "reconfigure"

    @property
    def _opnsense_item_class(self) -> type[DomainOverride]:
        return DomainOverride
