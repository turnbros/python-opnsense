from .alias_controller import FirewallAliasController
from .filter_controller import FilterController


class Firewall(object):

    def __init__(self, device):
        self._device = device

    @property
    def alias_controller(self) -> FirewallAliasController:
        return FirewallAliasController(self._device)

    @property
    def filter_controller(self) -> FilterController:
        return FilterController(self._device)
