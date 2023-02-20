import dns.resolver
import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from opnsense_api import Opnsense
from utils import query_opnsense_device_dns, compare

domain_ip_override = os.getenv("TEST_DOMAIN_IP")
test_alias = os.getenv("TEST_ALIAS")
test_domain = os.getenv("TEST_DOMAIN")
opnsense = Opnsense()


def test_domain_controller():
    # TODO: Finish the domain override test
    pass


def test_host_controller():
    # Make a note of the IP
    domain_start_ip = query_opnsense_device_dns(test_domain, 'A')
    host_overrides = opnsense.unbound_dns.host_override_controller

    # Make sure we're starting from a clean slate.
    override_list = host_overrides.list()
    assert len(override_list) == 0

    # ADD: Create the host override
    new_override = host_overrides.add("", test_domain, domain_ip_override, "test-override", True, "A")
    assert host_overrides.get(new_override.uuid).enabled is True
    assert compare(query_opnsense_device_dns(test_domain, 'A'), [domain_ip_override])

    # TOGGLE: Make sure we can disable the override
    host_overrides.toggle(new_override.uuid)
    assert host_overrides.get(new_override.uuid).enabled is False
    assert compare(query_opnsense_device_dns(test_domain, 'A'), domain_start_ip)

    # SET: Test set by enabling the override and updating the description without changes to the UUID
    old_override_uuid = new_override.uuid
    new_override = host_overrides.set(new_override.uuid, "", test_domain, domain_ip_override, "test-override-new", True, 'A')
    assert old_override_uuid == new_override.uuid
    assert compare(query_opnsense_device_dns(test_domain, 'A'), [domain_ip_override])

    # DELETE: Make sure we can delete the override and that the domain will
    # resolve to the IP it started with and that we end up with 0 overrides.
    host_overrides.delete(new_override.uuid)
    assert compare(query_opnsense_device_dns(test_domain, 'A'), domain_start_ip)
    assert len(host_overrides.list()) == 0


def test_alias_controller():

    # Make a note of the IP
    domain_start_ip = query_opnsense_device_dns(test_domain, 'A')
    host_overrides = opnsense.unbound_dns.host_override_controller
    alias_overrides = opnsense.unbound_dns.host_alias_controller

    # Make sure we're starting from a clean slate.
    host_override_list = host_overrides.list()
    assert len(host_override_list) == 0

    alias_override_list = alias_overrides.list()
    assert len(alias_override_list) == 0

    # ADD: Create the host override
    new_host_override = host_overrides.add("", test_domain, domain_ip_override, "test-override", True, "A")
    assert host_overrides.get(new_host_override.uuid).enabled is True
    assert compare(query_opnsense_device_dns(test_domain, 'A'), [domain_ip_override])

    new_host_alias = alias_overrides.add("", test_alias, new_host_override.uuid, "test-alias", True)
    assert compare(query_opnsense_device_dns(test_alias, 'A'), [domain_ip_override])

    # TOGGLE: Make sure we can disable the alias
    alias_overrides.toggle(new_host_alias.uuid)
    with pytest.raises(dns.resolver.NXDOMAIN):
        compare(query_opnsense_device_dns(test_alias, 'A'), domain_start_ip)

    # SET: Test set by enabling the alias and updating the description without changes to the UUID
    old_alias_uuid = new_host_alias.uuid
    new_host_alias = alias_overrides.set(new_host_alias.uuid, "", test_alias, new_host_override.uuid, "test-alias-new", True)
    assert old_alias_uuid == new_host_alias.uuid
    assert compare(query_opnsense_device_dns(test_domain, 'A'), [domain_ip_override])

    # DELETE: Make sure we can delete the override and that the domain will
    #         resolve to the IP it started with and that we end up with 0 overrides.
    # First delete the host alias
    alias_overrides.delete(new_host_alias.uuid)
    assert len(alias_overrides.list()) == 0
    # Then delete the host override
    host_overrides.delete(new_host_override.uuid)
    assert compare(query_opnsense_device_dns(test_domain, 'A'), domain_start_ip)
    assert len(host_overrides.list()) == 0
