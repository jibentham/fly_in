from dataclasses import dataclass, fieldt 
from typing import Any


@dataclass
class Hub:
    name: str
    x: int
    y: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Connection:
    start: Hub
    end: Hub
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Network:
    nb_drones: int
    start_hub: Hub
    end_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]


@dataclass
class Drone:
    id: int
    current_hub: Hub


@dataclass
class Simulation:
    network: Network
    drones: list[Drone]

