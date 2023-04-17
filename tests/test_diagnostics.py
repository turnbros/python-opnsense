import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from opnsense_api.diagnostics.system_diagnostics_controller import SystemActivity, SystemMemoryDetails
from opnsense_api.diagnostics.interface_diagnostics_controller import InterfaceSummary, InterfaceTopRecord, InterfaceTopRecordDetail, SystemRRDlist
from opnsense_api import Opnsense


domain_ip_override = os.getenv("TEST_DOMAIN_IP")
test_alias = os.getenv("TEST_ALIAS")
test_domain = os.getenv("TEST_DOMAIN")
opnsense = Opnsense()


def test_diagnostics_controller():

    opnsense_diagnostics = opnsense.diagnostics

    ### System Diagnostics ###
    opnsense_system_diagnostics = opnsense_diagnostics.system_diagnostics

    # System Activity
    system_activity = opnsense_system_diagnostics.get_activity()
    assert type(system_activity) is SystemActivity

    system_rrd_list = opnsense_diagnostics.interface_diagnostics.get_rrd_list()
    assert type(system_rrd_list) is SystemRRDlist
    assert system_rrd_list.result == "ok"
    assert len(system_rrd_list.packets) > 0
    assert len(system_rrd_list.system) > 0
    assert len(system_rrd_list.traffic) > 0

    ### Interface Diagnostics ###
    opnsense_interface_diagnostics = opnsense_diagnostics.interface_diagnostics
    assert len(opnsense_interface_diagnostics.list_interfaces()) > 0

    interface_summary = opnsense_interface_diagnostics.get_interface_summary()
    assert len(interface_summary) > 0
    assert type(interface_summary[0]) is InterfaceSummary

    interface_top = opnsense_interface_diagnostics.get_interface_top("lan")
    assert len(interface_top) > 0
    assert type(interface_top[0]) is InterfaceTopRecord
    assert len(interface_top[0].details) > 0
    assert type(interface_top[0].details[0]) is InterfaceTopRecordDetail

    ### Netflow Diagnostics ###
    opnsense_netflow_diagnostics = opnsense_diagnostics.netflow_diagnostics
    assert opnsense_netflow_diagnostics.get_status()["status"] == "inactive"


test_diagnostics_controller()
