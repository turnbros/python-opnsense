from enum import Enum
from typing import List, Union

from pydantic import Field

from .host_controller import HostOverride
from .resource_controller import UnboundResourceController
from ..util.item_controller import OPNsenseItem
from ..util.parse import parse_selected_keys


class HostAlias(OPNsenseItem):
    enabled: bool = True
    hostname: str
    domain: str
    host: Union[HostOverride, str] = Field(exclude=True)
    description: str = ""

    def _get_api_name(self):
        return "alias"

    def _get_api_representation(self) -> dict:
        d = super()._get_api_representation()
        if isinstance(self.host, str):
            d[self._get_api_name()] |= {"host": self.host}
        else:
            d[self._get_api_name()] |= {"host": self.host.uuid}
        return d

    @classmethod
    def _from_api_response_get(cls, api_response: dict, uuid: str, **kwargs) -> OPNsenseItem:
        return HostAlias(
            uuid=uuid,
            enabled=bool(int(api_response["enabled"])),
            host=parse_selected_keys(api_response["host"])[0],
            hostname=api_response["hostname"],
            domain=api_response["domain"],
            description=api_response["description"]
        )

    @classmethod
    def _from_api_response_list(cls, api_response: dict, **kwargs) -> OPNsenseItem:
        raise NotImplementedError("This method is not implemented!")


class AliasController(UnboundResourceController[HostAlias]):
    class _ItemActions(Enum):
        search = "searchHostAlias"
        get = "getHostAlias"
        add = "addHostAlias"
        set = "setHostAlias"
        delete = "delHostAlias"
        apply = "reconfigure"

    @property
    def _opnsense_item_class(self) -> type[HostAlias]:
        return HostAlias

    def list(self) -> List[HostAlias]:
        query_response = self._api_post(self._ItemActions.search.value)
        return [self.get(row["uuid"]) for row in query_response.get('rows')]
