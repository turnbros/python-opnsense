from __future__ import annotations
from typing import List

from opnsense_api.util.controller import OPNsenseAPIController
from dataclasses import dataclass


@dataclass
class InterfaceSummary:
    name: str  # "LAN"
    flags: str  # "8863"
    promiscuous_listeners: int  # "0"
    send_queue_length: int  # "0"
    send_queue_max_length: int  # "50"
    send_queue_drops: int  # "0"
    type: str  # "Ethernet"
    address_length: int  # "6"
    header_length: int  # "18"
    link_state: int  # "2"
    vhid: int  # "0"
    datalen: int  # "152"
    mtu: int  # "1500"
    metric: int  # "0"
    line_rate_bps: int  # "1000000000 bit/s
    packets_received: int  # "41638"
    input_errors: int  # "0"
    packets_transmitted: int  # "709"
    output_errors: int  # "0"
    collisions: int  # "0"
    bytes_received: int  # "2766217"
    bytes_transmitted: int  # "100767"
    multicasts_received: int  # "40961"
    multicasts_transmitted: "0"
    input_queue_drops: int  # "0"
    packets_for_unknown_protocol: int  # "0"
    hw_offload_capabilities: str  # "0x0"
    uptime_at_attach_or_stat_reset: int  # "1"

    @classmethod
    def from_json(cls, data) -> InterfaceSummary:
        return InterfaceSummary(
            data["name"],
            data["flags"],
            data["promiscuous listeners"],
            data["send queue length"],
            data["send queue max length"],
            data["send queue drops"],
            data["type"],
            data["address length"],
            data["header length"],
            data["link state"],
            data["vhid"],
            data["datalen"],
            data["mtu"],
            data["metric"],
            data["line rate"],
            data["packets received"],
            data["input errors"],
            data["packets transmitted"],
            data["output errors"],
            data["collisions"],
            data["bytes received"],
            data["bytes transmitted"],
            data["multicasts received"],
            data["multicasts transmitted"],
            data["input queue drops"],
            data["packets for unknown protocol"],
            data["HW offload capabilities"],
            data["uptime at attach or stat reset"]
        )


@dataclass
class InterfaceTopRecordDetail:
    address: str
    rate: str
    rate_bits: int
    cumulative: str
    cumulative_bytes: int
    tags: List[str]

    @classmethod
    def from_json(cls, data) -> InterfaceTopRecordDetail:
        return InterfaceTopRecordDetail(
            data["address"],
            data["rate"],
            data["rate_bits"],
            data["cumulative"],
            data["cumulative_bytes"],
            data["tags"])


@dataclass
class InterfaceTopRecord:
    name: str
    address: str
    rate_in: str
    rate_out: str
    rate: str
    cumulative_in: str
    cumulative_out: str
    cumulative: str
    rate_bits_in: int
    rate_bits_out: int
    rate_bits: int
    cumulative_bytes_in: int
    cumulative_bytes_out: int
    cumulative_bytes: int
    tags: List[str]
    details: List[InterfaceTopRecordDetail]

    @classmethod
    def from_json(cls, data) -> InterfaceTopRecord:
        client_details = []
        for client_detail in data["details"]:
            client_details.append(InterfaceTopRecordDetail.from_json(client_detail))

        return InterfaceTopRecord(
            data["rname"],
            data["address"],
            data["rate_in"],
            data["rate_out"],
            data["rate"],
            data["cumulative_in"],
            data["cumulative_out"],
            data["cumulative"],
            data["rate_bits_in"],
            data["rate_bits_out"],
            data["rate_bits"],
            data["cumulative_bytes_in"],
            data["cumulative_bytes_out"],
            data["cumulative_bytes"],
            data["tags"],
            client_details
        )


@dataclass
class SystemRRDlist:
    result: str
    packets: List[str]
    system: List[str]
    traffic: List[str]

    @classmethod
    def from_json(cls, data) -> SystemRRDlist:
        return cls(data["result"],
                   data["data"]["packets"],
                   data["data"]["system"],
                   data["data"]["traffic"])


class InterfaceDiagnosticsController:

    def __init__(self, device):
        self._system_health_controller = self._SystemHealth(device)
        self._traffic_controller = self._Traffic(device)

    def list_interfaces(self) -> List[str]:
        """
        Lists the configured interfaces

        :return: SystemInterfaces
        """
        return self._system_health_controller.get_interfaces()

    def get_interface_summary(self) -> List[InterfaceSummary]:
        """
        Returns a list of interfaces and their utilization.

        :return:
        """
        return self._traffic_controller.interface()

    def get_interface_top(self, interface) -> List[InterfaceTopRecord]:
        """
        Returns detailed information about a specific interface.

        :param interface:
        :return:
        """
        return self._traffic_controller.top(interface)

    def get_rrd_list(self) -> SystemRRDlist:
        """
        Returns a list of data being collected by the RRD.
        More information on RRD can be found here: https://oss.oetiker.ch/rrdtool/index.en.html

        :return: SystemRRDlist
        """
        return self._system_health_controller.get_rrd_list()

    class _SystemHealth(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "systemhealth")

        def get_interfaces(self) -> List[str]:
            return self._api_get("getInterfaces").keys()

        def get_rrd_list(self) -> SystemRRDlist:
            return SystemRRDlist.from_json(self._api_get("getRRDlist"))

    class _Traffic(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "traffic")

        def interface(self) -> List[InterfaceSummary]:
            api_interfaces = self._api_get("Interface")
            interfaces = []
            for interface in api_interfaces["interfaces"]:
                interfaces.append(InterfaceSummary.from_json(api_interfaces["interfaces"][interface]))
            return interfaces

        def top(self, interface) -> List[InterfaceTopRecord]:

            api_response = self._api_get("top", interface)
            if len(api_response) == 0:
                raise Exception(f"Interface \"{interface}\" not found!")

            api_response = api_response[interface]
            if api_response["status"] != "ok":
                raise Exception(f"Failed to get interface top! Status: {api_response['status']}")

            interface_top_records = []
            for interface_top_record in api_response["records"]:
                interface_top_records.append(InterfaceTopRecord.from_json(interface_top_record))

            return interface_top_records




