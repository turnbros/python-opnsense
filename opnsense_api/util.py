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

def parse_query_response_alias(alias):
  name = alias["name"]
  description = alias["description"]
  enabled = bool(int(alias['enabled']))

  counters = alias["counters"]
  updatefreq = alias["updatefreq"]

  parsed_alias_type = None
  for alias_type in alias["type"].keys():
    if alias["type"][alias_type]["selected"] == 1:
      parsed_alias_type = alias_type.upper()
      break

  parsed_alias_proto = None
  for alias_proto in alias["proto"].keys():
    if alias["proto"][alias_proto]["selected"] == 1:
      parsed_alias_proto = alias_proto.upper()
      break

  parsed_alias_content = []
  for alias_content in alias["content"].keys():
    if alias["content"][alias_content]["selected"] == 1:
      parsed_alias_content.append(alias["content"][alias_content]["value"])

  return {
    "name": name,
    "type": parsed_alias_type,
    "description": description,
    "updatefreq": updatefreq,
    "counters": counters,
    "proto": parsed_alias_proto,
    "content": parsed_alias_content,
    "enabled": enabled
  }

