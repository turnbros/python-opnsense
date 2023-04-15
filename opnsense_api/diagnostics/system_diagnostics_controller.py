from __future__ import annotations
from dataclasses import dataclass
from typing import List

from opnsense_api.util.controller import OPNsenseAPIController


@dataclass
class ThreadStats:
    total: int
    running: int
    sleeping: int
    waiting: int

    @classmethod
    def from_json(cls, data) -> ThreadStats:
        pass


@dataclass
class CPUStats:
    user: float
    nice: float
    system: float
    interrupt: float
    idle: float

    @classmethod
    def from_json(cls, data) -> CPUStats:
        pass


@dataclass
class MemoryStats:
    active: int
    inactive: int
    wired: int
    buffered: int
    free: int

    @classmethod
    def from_json(cls, data) -> MemoryStats:
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

    @classmethod
    def from_json(cls, data) -> ProcessStats:
        pass


@dataclass
class SystemActivity:
    last_pid: int
    load_averages: List[int]
    uptime: int
    thread_stats: ThreadStats
    cpu_stats: CPUStats
    memory_stats: MemoryStats
    system_processes: List[ProcessStats]

    @classmethod
    def from_json(cls, data) -> SystemActivity:
        pass


@dataclass
class SystemMemoryAllocationDetails:
    name: str
    in_use: int
    memory_use: int
    requests: int
    size: List[int]

    @classmethod
    def from_json(cls, data) -> SystemMemoryAllocationDetails:
        return SystemMemoryAllocationDetails(data["name"],
                                             data["in-use"],
                                             data["memory-use"],
                                             data["requests"],
                                             data["size"])


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

    @classmethod
    def from_json(cls, data) -> SystemMemoryZoneStatistics:
        return SystemMemoryZoneStatistics(data["name"],
                                          data["size"],
                                          data["limit"],
                                          data["used"],
                                          data["free"],
                                          data["requests"],
                                          data["fail"],
                                          data["sleep"],
                                          data["xdomain"])


@dataclass
class SystemMemoryDetails:

    memory_allocations: List[SystemMemoryAllocationDetails]
    total_allocated_memory_used: int

    virtual_memory_zones: List[SystemMemoryZoneStatistics]
    total_virtual_memory_used: int

    @classmethod
    def from_json(cls, data) -> SystemMemoryDetails:
        memory_allocations = []
        for allocation_json in data["malloc-statistics"]["memory"]:
            memory_allocations.append(SystemMemoryAllocationDetails.from_json(allocation_json))
        total_allocated_memory_used = data["malloc-statistics"]["totals"]["used"]

        virtual_memory_zones = []
        for zone_json in data["memory-zone-statistics"]["zone"]:
            virtual_memory_zones.append(SystemMemoryZoneStatistics.from_json(zone_json))
        total_virtual_memory_used = data["memory-zone-statistics"]["totals"]["used"]

        return cls(memory_allocations,
                   total_allocated_memory_used,
                   virtual_memory_zones,
                   total_virtual_memory_used)


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
        Returns detailed system memory statistics.

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
            return SystemMemoryDetails.from_json(self._api_get("memory"))
