import logging
import urllib.parse
from enum import Enum
from typing import TypedDict

log = logging.getLogger(__name__)


class RecordType(Enum):
    A = "A"
    AAAA = "AAAA"
    MX = "MX"


class BoundOverride(TypedDict):
    uuid: str
    hostname: str


class HostAlias(TypedDict):
  uuid: str
  hostname: str
  domain: str
  description: str
  host: BoundOverride
  enabled: bool


class DomainOverride(TypedDict):
  uuid: str
  domain: str
  server: str
  description: str
  enabled: bool


class HostOverride(TypedDict):
  uuid: str
  hostname: str
  domain: str
  server: str
  rr: RecordType
  mxprio: str
  mx: str
  description: str
  enabled: bool


def parse_unbound_resource(kind: str, uuid: str, resource: dict):
  if kind == "alias":
    return parse_unbound_host_alias(uuid, resource)
  if kind == "host":
    return parse_unbound_host_override(uuid, resource)
  if kind == "domain":
    return parse_unbound_domain_override(uuid, resource)


def parse_unbound_host_alias(uuid: str, alias: dict) -> HostAlias:
    """

    :param uuid:
    :param alias:
    :return: HostAlias
    """
    bound_host_uuid = None
    bound_hostname = None
    for host_uuid in alias["host"].keys():
        if alias["host"][host_uuid]["selected"] == 1:
            bound_host_uuid = host_uuid
            bound_hostname = alias["host"][host_uuid]["value"]
            break

    # None evals to False.
    if not all([bound_host_uuid, bound_hostname]):
        log.error(f"Unable to determine which host this alias is bound to!\n"
                  f"bound_host_uuid: {bound_host_uuid}\n"
                  f"bound_hostname: {bound_hostname}\n")
        raise Exception("Failed to parse the alias host override. ")

    return HostAlias(
        uuid=uuid,
        hostname=alias["hostname"],
        description=alias["description"],
        domain=alias["domain"],
        host=BoundOverride(
            uuid=bound_host_uuid,
            hostname=bound_hostname
        ),
        enabled=bool(int(alias['enabled']))
    )


def parse_unbound_domain_override(uuid: str, domain: dict) -> DomainOverride:
    """

    :param uuid:
    :param domain:
    :return: DomainOverride
    """
    return DomainOverride(
        uuid=uuid,
        domain=domain['domain'],
        server=domain['server'],
        description=domain['description'],
        enabled=bool(int(domain['enabled'])),
    )


def parse_unbound_host_override(uuid: str, host: dict) -> HostOverride:
    """

    :param uuid:
    :param host:
    :return: HostOverride
    """
    record_type = None
    for resource_record_type in host["rr"].keys():
        if host["rr"][resource_record_type]["selected"] == 1:
            record_type = resource_record_type

    # None evals to False.
    if not record_type:
        log.error(f"Unable to determine the host overrides record type!\n"
                  f"record_type: {record_type}\n")
        raise Exception("Failed to parse the alias host override. ")

    host['enabled'] = bool(int(host['enabled']))
    return HostOverride(
        uuid=uuid,
        enabled=bool(int(host['enabled'])),
        hostname=host['hostname'],
        domain=host['domain'],
        rr=record_type,
        mxprio=host['mxprio'],
        mx=host['mx'],
        server=host['server'],
        description=host['description']
    )


def format_request(module: str, controller: str, command: str, uuid: str = None, params: dict = {}) -> str:
    """

    :param module: str
    :param controller: str
    :param command: str
    :param uuid: str
    :param params: dict

    :return: str
    """
    # Simplest url path for a request
    # e.g. api/unbound/settings/searchHostOverride
    base_request = f"{module}/{controller}/{command}"

    # Add in the UUID for a specific resource
    # e.g. api/unbound/settings/getHostOverride/2ce9672e-43a5-4462-9cf1-084964970862
    if uuid is not None:
        base_request = f"{module}/{controller}/{command}/{uuid}"

    # Sprinkle some url params on top.
    # e.g. api/unbound/settings/toggleHostOverride/2ce9672e-43a5-4462-9cf1-084964970862
    if len(params.keys()) > 0:
        base_request = f"{base_request}?{urllib.parse.urlencode(params)}"

    return base_request
