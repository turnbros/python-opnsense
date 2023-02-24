from typing import Optional

class FailedToParseItemException(Exception):
    def __init__(self, class_type: str, msg: str):
        super().__init__(f"Failed to parse {class_type}: {msg}")


class FailedToDeleteException(Exception):
    def __init__(self, class_name: str, uuid: str, query_response: dict):
        super().__init__(f"Failed to delete {class_name} with UUID {uuid} with reason: "
                         f"{query_response}")


class FailedToApplyChangesException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class ItemNotFoundException(Exception):
    def __init__(self, class_name: str, uuid: str, query_response: dict):
        super().__init__(f"Could not find {class_name} with uuid {uuid} with reason: {query_response}")


class FailedToAddItemException(Exception):
    def __init__(self, class_name: str, uuid: str, query_response: dict):
        super().__init__(f"Failed to set {class_name} with UUID {uuid} with reason: "
                         f"{query_response}")


class FailedToSetItemException(Exception):
    def __init__(self, class_name: str, uuid: str, query_response: dict):
        super().__init__(f"Failed to add {class_name} with UUID {uuid} with reason: "
                         f"{query_response}")


class InvalidItemException(ValueError):
    def __init__(self, class_name: str, field: str = "", value: str = "", valid_values: Optional[list[str]] = None,
                 custom_message: str = ""):
        if not custom_message:
            super().__init__(
                f"Invalid {class_name}:\nValue for '{field}' is '{value}' but should be one of {valid_values}")
        else:
            super().__init__(f"Invalid {class_name}:\n{custom_message}")
