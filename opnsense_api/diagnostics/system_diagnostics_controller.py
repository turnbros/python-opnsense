from opnsense_api.util.controller import OPNsenseAPIController
from opnsense_api.diagnostics.diagnostics_dataclasses import SystemMemory, SystemActivity


class SystemDiagnosticsController:

    def __init__(self, device):
        self._system_activity_controller = self._SystemActivity(device)
        self._system_memory_controller = self._SystemMemory(device)

    def get_activity(self) -> SystemActivity:
        """
        Returns detailed information about system utilization and process state

        :return: SystemActivity
        """
        return self._system_activity_controller.get_activity()

    def get_memory_statistics(self) -> SystemMemory:
        """
        Returns system memory statistics.

        :return: SystemMemory
        """
        return self._system_memory_controller.get_memory()

    class _SystemActivity(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "activity")

        def get_activity(self) -> SystemActivity:
            return self._api_get("getActivity")

    class _SystemMemory(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "system")

        def get_memory(self) -> SystemMemory:
            return self._api_get("memory")
