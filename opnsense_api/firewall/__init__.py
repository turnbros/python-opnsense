from .alias_controller import Alias
from .filter_controller import Filter
from .category_controller import CategoryController


class Firewall(object):

    def __init__(self, device):
        self._device = device

    @property
    def alias_controller(self) -> Alias:
        return Alias(self._device)

    @property
    def filter_controller(self) -> Filter:
        return Filter(self._device)

    @property
    def category_controller(self) -> CategoryController:
        return CategoryController(self._device)
