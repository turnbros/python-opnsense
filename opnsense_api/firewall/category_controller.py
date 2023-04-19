import re

from pydantic import constr, validator

from opnsense_api.util.exceptions import InvalidItemException
from opnsense_api.util.item_controller import OPNsenseItem, OPNsenseItemController


class Category(OPNsenseItem):
    """
    Represents a firewall category in an OPNsense device.

    """

    name: str
    auto: bool = True
    color: constr(to_lower=True, max_length=6) = ""

    @validator("color", always=True)
    def color_valid(cls, value):
        valid_color_regex = r'([a-f0-9]{6}|^$)'
        if not re.fullmatch(valid_color_regex, value):
            raise InvalidItemException("Category", custom_message="Value for 'color' should either be '' "
                                                                  "or a six character long hex string.")
        return value


class CategoryController(OPNsenseItemController[Category]):

    def __init__(self, device):
        super().__init__(device, "firewall", "category")

    @property
    def _opnsense_item_class(self) -> type[Category]:
        return Category
