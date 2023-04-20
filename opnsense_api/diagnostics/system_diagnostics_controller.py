from __future__ import annotations

from dataclasses import dataclass
from typing import List
import re

from opnsense_api.util.controller import OPNsenseAPIController


@dataclass
class ThreadStats:
    """
    ThreadStats

    """
    total: int
    running: int
    sleeping: int
    waiting: int

    @classmethod
    def _parse(cls, data) -> ThreadStats:
        # Parses 160 threads:   3 running, 109 sleeping, 48 waiting
        pattern = "^(?P<total_threads>\d+)\sthreads\W+(?P<running_threads>\d+)\srunning\W+(?P<sleeping_threads>\d+)\ssleeping\W+(?P<waiting_threads>\d+)\swaiting"
        data_dict = re.search(pattern, data).groupdict()
        return cls(int(data_dict["total_threads"]),
                   int(data_dict["running_threads"]),
                   int(data_dict["sleeping_threads"]),
                   int(data_dict["waiting_threads"]))


@dataclass
class CPUStats:
    """
    CPUStats

    """
    user: float
    nice: float
    system: float
    interrupt: float
    idle: float

    @classmethod
    def _parse(cls, data) -> CPUStats:
        # Parses CPU:  2.7% user,  0.0% nice,  4.9% system,  0.0% interrupt, 92.4% idle
        pattern = "^CPU\W+(?P<cpu_util_user>[+-]?([0-9]*[.])?[0-9]+)\W+user\W+(?P<cpu_util_nice>[+-]?([0-9]*[.])?[0-9]+)\W+nice\W+(?P<cpu_util_system>[+-]?([0-9]*[.])?[0-9]+)\W+system\W+(?P<cpu_util_interrupt>[+-]?([0-9]*[.])?[0-9]+)\W+interrupt\W+(?P<cpu_util_idle>[+-]?([0-9]*[.])?[0-9]+)\W+idle"
        data_dict = re.search(pattern, data).groupdict()
        return cls(float(data_dict["cpu_util_user"]),
                   float(data_dict["cpu_util_nice"]),
                   float(data_dict["cpu_util_system"]),
                   float(data_dict["cpu_util_interrupt"]),
                   float(data_dict["cpu_util_idle"]))


@dataclass
class MemoryStats:
    """
    MemoryStats

    """
    active: int
    inactive: int
    wired: int
    buffered: int
    free: int

    @classmethod
    def _parse(cls, data) -> MemoryStats:
        # Parses Mem: 93M Active, 23M Inact, 254M Wired, 88M Buf, 3553M Free
        pattern = "^Mem\W+(?P<memory_active_mb>\d+)M\W+Active\W+(?P<memory_inactive_mb>\d+)M\W+Inact\W+(?P<memory_wired_mb>\d+)M\W+Wired\W+(?P<memory_buffered_mb>\d+)M\W+Buf\W+(?P<memory_free_mb>\d+)M\W+Free"
        data_dict = re.search(pattern, data).groupdict()
        return cls(int(data_dict["memory_active_mb"]),
                   int(data_dict["memory_inactive_mb"]),
                   int(data_dict["memory_wired_mb"]),
                   int(data_dict["memory_buffered_mb"]),
                   int(data_dict["memory_free_mb"]))


@dataclass
class ProcessStats:
    """
    ProcessStats

    """
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
    def _parse(cls, data) -> ProcessStats:
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
    """
    SystemActivity

    """
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
    def _parse(cls, data) -> SystemActivity:
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

        thread_stats = ThreadStats._parse(data["headers"][1])
        cpu_stats = CPUStats._parse(data["headers"][2])
        memory_stats = MemoryStats._parse(data["headers"][3])

        system_processes = []
        for process_json in data["details"]:
            system_processes.append(ProcessStats._parse(process_json))

        return SystemActivity(int(last_pid),
                              float(load_average_1m),
                              float(load_average_5m),
                              float(load_average_15m),
                              int(uptime),
                              system_time,
                              thread_stats,
                              cpu_stats,
                              memory_stats,
                              system_processes)


@dataclass
class SystemMemoryAllocationDetails:
    """
    SystemMemoryAllocationDetails

    """
    name: str
    in_use: int
    memory_use: int
    requests: int
    size: List[int]

    @classmethod
    def _parse(cls, data) -> SystemMemoryAllocationDetails:
        return SystemMemoryAllocationDetails(data["name"],
                                             int(data["in-use"]),
                                             int(data["memory-use"]),
                                             int(data["requests"]),
                                             data["size"])


@dataclass
class SystemMemoryZoneStatistics:
    """
    SystemMemoryZoneStatistics

    """

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
    def _parse(cls, data) -> SystemMemoryZoneStatistics:
        return SystemMemoryZoneStatistics(data["name"],
                                          int(data["size"]),
                                          int(data["limit"]),
                                          int(data["used"]),
                                          int(data["free"]),
                                          int(data["requests"]),
                                          int(data["fail"]),
                                          int(data["sleep"]),
                                          int(data["xdomain"]))


@dataclass
class SystemMemoryDetails:
    """
    SystemMemoryDetails

    """
    memory_allocations: List[SystemMemoryAllocationDetails]
    total_allocated_memory_used: int

    virtual_memory_zones: List[SystemMemoryZoneStatistics]
    total_virtual_memory_used: int

    @classmethod
    def _parse(cls, data) -> SystemMemoryDetails:
        memory_allocations = []
        for allocation_json in data["malloc-statistics"]["memory"]:
            memory_allocations.append(SystemMemoryAllocationDetails._parse(allocation_json))
        total_allocated_memory_used = data["malloc-statistics"]["totals"]["used"]

        virtual_memory_zones = []
        for zone_json in data["memory-zone-statistics"]["zone"]:
            virtual_memory_zones.append(SystemMemoryZoneStatistics._parse(zone_json))
        total_virtual_memory_used = data["memory-zone-statistics"]["totals"]["used"]

        return cls(memory_allocations,
                   int(total_allocated_memory_used),
                   virtual_memory_zones,
                   int(total_virtual_memory_used))


@dataclass
class SystemRRDlist:
    """
    Contains lists of system and interface for which metrics are being collected.

    """

    #: A list of interfaces being monitored for packet metrics
    packets: List[str]
    #: A list of system processes being monitored for utilization metrics
    system: List[str]
    #: A list of interfaces being monitored for traffic metrics
    traffic: List[str]

    @classmethod
    def _parse(cls, data) -> SystemRRDlist:
        if data["result"] != "ok":
            raise Exception(f"Failed to parse System RRD List!\n Error: {data['result']}")
        return cls(data["data"]["packets"],
                   data["data"]["system"],
                   data["data"]["traffic"])


class SystemDiagnosticsController:

    def __init__(self, device):
        self._system_activity_controller = self._SystemActivity(device)
        self._system_memory_controller = self._SystemMemory(device)

    def get_activity(self) -> SystemActivity:
        """
        Returns detailed information about system utilization and process state

        """
        return self._system_activity_controller.get_activity()

    # def get_memory_statistics(self) -> SystemMemoryDetails:
    #     """
    #     Returns detailed system memory statistics.
    #
    #     """
    #     return self._system_memory_controller.get_memory_details()

    def get_rrd_list(self) -> SystemRRDlist:
        """
        Returns a list of data being collected by the RRD.
        More information on RRD can be found here: https://oss.oetiker.ch/rrdtool/index.en.html

        """
        return self._system_health_controller.get_rrd_list()

    class _SystemActivity(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "activity")

        def get_activity(self) -> SystemActivity:
            return SystemActivity._parse(self._api_get("getActivity"))

    class _SystemMemory(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "system")

        def get_memory_details(self) -> SystemMemoryDetails:
            return SystemMemoryDetails._parse(self._api_get("memory"))

    class _SystemHealth(OPNsenseAPIController):

        def __init__(self, device):
            super().__init__(device, "diagnostics", "systemhealth")

        def get_rrd_list(self) -> SystemRRDlist:
            return SystemRRDlist._parse(self._api_get("getRRDlist"))
