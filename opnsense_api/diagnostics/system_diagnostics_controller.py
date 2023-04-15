from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re

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
        return ProcessStats(data["C"],
                            data["PID"],
                            data["THR"],
                            data["USERNAME"],
                            data["PRI"],
                            data["NICE"],
                            data["SIZE"],
                            data["RES"],
                            data["STATE"],
                            data["TIME"],
                            data["WCPU"],
                            data["COMMAND"])


@dataclass
class SystemActivity:
    last_pid: int
    load_average_1m: float
    load_average_5m: float
    load_average_15m: float
    uptime: int
    system_time: str
    thread_stats: ThreadStats
    cpu_stats: CPUStats
    memory_stats: MemoryStats
    system_processes: List[ProcessStats]

    @classmethod
    def from_json(cls, data) -> SystemActivity:
        # Parse "last pid: 45701;  load averages:  0.26,  0.43,  0.41  up 59+06:39:49    23:03:19"
        pid_avgs_up_json = data["headers"][0]
        pattern = "^last pid:\s+(?P<last_pid>\d+)\W+load averages:\s+(?P<load_avg_1m>[+-]?([0-9]*[.])?[0-9]+)\W+(?P<load_avg_5m>[+-]?([0-9]*[.])?[0-9]+)\W+(?P<load_avg_15m>[+-]?([0-9]*[.])?[0-9]+)\W+up\s+(?P<uptime_days>\d+)\+(?P<uptime_hours>\d+):(?P<uptime_minutes>\d+):(?P<uptime_seconds>\d+)\W+(?P<system_time>\d{2}:\d{2}:\d{2})"
        pid_avgs_up_dict = re.search(pattern, pid_avgs_up_json).groupdict()

        last_pid = pid_avgs_up_dict["last_pid"]
        load_average_1m = pid_avgs_up_dict["load_avg_1m"]
        load_average_5m = pid_avgs_up_dict["load_avg_5m"]
        load_average_15m = pid_avgs_up_dict["load_avg_15m"]
        system_time = pid_avgs_up_dict["system_time"]

        uptime = (int(pid_avgs_up_dict["uptime_days"]) * 86400) + \
                 (int(pid_avgs_up_dict["uptime_hours"]) * 3600) + \
                 (int(pid_avgs_up_dict["uptime_minutes"]) * 60) + \
                 (int(pid_avgs_up_dict["uptime_seconds"]))

        thread_stats = ThreadStats.from_json(data["headers"][1])
        cpu_stats = CPUStats.from_json(data["headers"][2])
        memory_stats = MemoryStats.from_json(data["headers"][3])

        system_processes = []
        for process_json in data["details"]:
            system_processes.append(ProcessStats.from_json(process_json))

        return SystemActivity(last_pid,
                              load_average_1m,
                              load_average_5m,
                              load_average_15m,
                              uptime,
                              system_time,
                              thread_stats,
                              cpu_stats,
                              memory_stats,
                              system_processes)


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
