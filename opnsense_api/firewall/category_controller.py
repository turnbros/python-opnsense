import pydantic


class Category(pydantic.BaseModel):
    uuid: str = ""
    name: str
    auto: str
    color: str = ""

    class InvalidCategoryException(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    @pydantic.validator("auto")
    @classmethod
    def auto_valid(cls, value: str) -> str:
        if value not in ["0", "1"]:
            raise Category.InvalidCategoryException("Value for 'auto' should be either '0' or '1'.")
        return value

    @pydantic.validator("color")
    @classmethod
    def color_valid(cls, value: str) -> str:
        value = value.lower()
        if len(value) not in [0, 6]:
            raise Category.InvalidCategoryException("Value for 'color' should either be '' or a six character long "
                                                    "hex string.")
        for c in value:
            if c not in "0123456789abcdef":
                raise Category.InvalidCategoryException("Value for 'color' should either be '' or a six character long "
                                                        "hex string.")
        return value


class CategoryController(object):

    def __init__(self, device):
        self.__device = device

    def get(self, uuid: str = None) -> Category | None:
        query_results = self.__device._authenticated_request("GET", f"firewall/category/getItem/{uuid}")

        if "category" not in query_results:
            return None

        category = query_results["category"]
        try:
            return Category(uuid=uuid, name=category.get("name"), auto=category.get("auto"),
                            color=category.get("color"))
        except Category.InvalidCategoryException:
            return None

    def add(self, category: Category) -> None:
        response = self.__device._authenticated_request("POST", "firewall/category/addItem",
                                                        body={"category": dict(category)})
        if response["result"] != "saved":
            raise Exception(f"Failed to add category. Reason: {response}")
        category.uuid = response["uuid"]

    def list(self) -> list[Category]:
        query_results = self.__device._authenticated_request("GET", "firewall/category/get")
        categories = query_results['category']['categories']['category']
        return [Category.parse_obj({'uuid': category_uuid} | categories.get(category_uuid))
                for category_uuid in categories]

    def set(self, category: Category) -> None:
        existing_category = self.get(category.uuid)
        if existing_category is None:
            raise Exception(f"Category with UUID {category.uuid} not found")

        response = self.__device._authenticated_request("POST", f"firewall/category/setItem/{category.uuid}",
                                                        body={"category": dict(category)})
        if response["result"] != "saved":
            raise Exception(f"Failed to set category. Reason: {response}")

    def delete(self, category: str | Category):
        response = self.__device._authenticated_request("POST", "firewall/category/delItem/"
                                                        f"{category if isinstance(category, str) else category.uuid}")
        if response["result"] != "deleted":
            raise Exception(f"Failed to delete category. Reason: {response}")
