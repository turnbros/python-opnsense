import base64
from enum import Enum


class Constants(object):
    HTTP_SUCCESS = [200, 201, 202, 203, 204, 205, 206, 207]


class AliasType(Enum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"


class ProtocolType(Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class ParsingError(Exception):
    def __init__(self, uuid, element, msg):
        self.uuid = uuid
        self.element = element
        super().__init__(msg)


def reliable_b64_decode(string):
    try:
        return base64.b64decode(string).decode("utf-8")
    except Exception:
        return string
