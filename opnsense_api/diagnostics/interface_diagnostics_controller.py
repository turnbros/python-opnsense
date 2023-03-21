from opnsense_api.diagnostics.diagnostics_dataclasses import SystemInterfaces, SystemRRDlist
from opnsense_api.util.controller import OPNsenseAPIController


class InterfaceDiagnosticsController:

    def __init__(self, device):
        self._system_health_controller = self._SystemHealth(device)
        self._traffic_controller = self._Traffic(device)

    def list_interfaces(self) -> SystemInterfaces:
        """
        Lists the configured interfaces

        :return: SystemInterfaces
        """
        return self._system_health_controller.get_interfaces()

    def get_interfaces(self):
        """
        Returns a list of interfaces and their utilization

        :return:
        """
        return self._traffic_controller.interface()

    def get_interface(self, interface):
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

        def get_interfaces(self) -> SystemInterfaces:
            return self._api_get("getInterfaces")

        def get_rrd_list(self) -> SystemRRDlist:
            return self._api_get("getRRDlist")

    class _Traffic(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "traffic")

        def interface(self) -> SystemInterfaces:
            return self._api_get("Interface")

        def top(self, interface) -> SystemRRDlist:
            return self._api_get("Top", interface)
