from dataclasses import dataclass
from typing import List

from opnsense_api.util.controller import OPNsenseAPIController


@dataclass
class ThreadStats:
    total: int
    running: int
    sleeping: int
    waiting: int


@dataclass
class MemoryStats:
    pass


@dataclass
class CPUStats:
    pass


@dataclass
class ProcessStats:
    c: str  # "0"
    pid: str  # "11"
    thr: str  # "100003"
    username: str  # "root"
    pri: str  # "155"
    nice: str  # "ki31"
    size: str  # "0B"
    res: str  # "32K"
    state: str  # "RUN"
    time: str  # "281.3H"
    wcpu: str  # "98.08%"
    command: str  # "[idle{idle: cpu0}]"


@dataclass
class SystemActivity:
    last_pid: int
    load_averages: List[int]
    uptime: int
    thread_stats: ThreadStats
    cpu_stats: CPUStats
    memory_stats: MemoryStats
    system_processes: List[ProcessStats]


@dataclass
class SystemMemoryAllocationDetails:
    name: str
    in_use: int
    memory_use: int
    requests: int
    size: List[int]


@dataclass
class SystemMemoryZoneStatistics:
    name: str
    size: int
    limit: int
    used: int
    free: int
    requests: int
    fail: int
    sleep: int
    xdomain: int


@dataclass
class SystemMemoryDetails:

    memory_allocations: List[SystemMemoryAllocationDetails]
    total_allocated_memory_used: int

    virtual_memory_zones: List[SystemMemoryZoneStatistics]
    total_virtual_memory_used: int


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

    def get_memory_statistics(self) -> SystemMemoryDetails:
        """
        Returns system memory statistics.

        :return: SystemMemoryDetails
        """
        return self._system_memory_controller.get_memory_details()

    class _SystemActivity(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "activity")

        def get_activity(self) -> SystemActivity:
            return self._api_get("getActivity")

    class _SystemMemory(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "system")

        def get_memory_details(self) -> SystemMemoryDetails:
            return self._api_get("memory")
