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
