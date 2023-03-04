from .alias_controller import AliasController
from .domain_controller import DomainController
from .host_controller import HostController


class Unbound(object):

    def __init__(self, device):
        self._device = device

    @property
    def host_alias_controller(self) -> AliasController:
        return AliasController(self._device)

    @property
    def host_override_controller(self) -> HostController:
        return HostController(self._device)

    @property
    def domain_override_controller(self) -> DomainController:
        return DomainController(self._device)
