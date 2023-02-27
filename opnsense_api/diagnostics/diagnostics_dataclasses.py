from dataclasses import dataclass
from typing import List


@dataclass
class SystemProcess:
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


@dataclass()
class SystemActivity:
    system_processes: List[SystemProcess]


@dataclass()
class SystemMemory:
    pass


@dataclass()
class SystemInterfaces:
    name: str
    description: str


@dataclass()
class SystemRRDlist:
    pass
