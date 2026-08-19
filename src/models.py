from __future__ import annotations
from dataclasses import dataclass, field 
from typing import Any


@dataclass
class Hub:
    name: str
    x: int
    y: int
    nb_occupants: int
    occupants: list[Drone] = field(default_factory=list)
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
    drones: list[Drone]

