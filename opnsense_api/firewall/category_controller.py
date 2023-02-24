import re
from typing import Optional

from pydantic import constr, validator

from opnsense_api.util.exceptions import InvalidItemException, FailedToParseItemException
from opnsense_api.util.item_controller import OPNSenseItem, TOPNSenseItem, OPNSenseItemController


class Category(OPNSenseItem):
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

    @classmethod
    def from_api_response_list(cls, api_response: dict, **kwargs) -> OPNSenseItem:
        return Category.parse_obj(api_response)

    @classmethod
    def from_api_response_get(cls, api_response: dict, uuid: Optional[str] = None, **kwargs) -> TOPNSenseItem:
        if uuid is None:
            raise FailedToParseItemException("Category", "Can't parse Category if no UUID is passed.")

        return Category.parse_obj({"uuid": uuid} | api_response)


class CategoryController(OPNSenseItemController):

    def __init__(self, device):
        super().__init__(device, "firewall", "category")

    @property
    def opnsense_item_class(self) -> type[Category]:
        return Category
