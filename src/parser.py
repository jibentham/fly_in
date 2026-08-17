from pathlib import Path
from collections import defaultdict
from typing import Any


def str_to_int(value: str) -> Any:
    """Convert numeric strings to integers
     or return the string if unconvertable"""
    try:
        return int(value)
    except ValueError:
        return value


def parse_metadata(data: str) -> dict[str, Any]:
    """Format optional metadata for each zone as a dictionary"""
    data = data.strip().strip("[]")
    metadata: dict[str, Any] = {}

    if not data:
        return metadata
    for tag in data.split():
        key, value = tag.split("=", 1)
        metadata[key] = str_to_int(value)
    return metadata


def parse_hub(data: str) -> dict[str, Any]:
    if "[" in data:
        main, metadata = data.split("[", 1)
        metadata = "[" + metadata
    else:
        main = data
        metadata = ""
    values = main.split()
    name: str = values[0]
    x: int = int(values[1])
    y: int = int(values[2])
    hub: dict[str, Any] = {
        "name": name,
        "x": x,
        "y": y,
    }
    hub.update(parse_metadata(metadata))
    return hub


def parse_connection(data: str) -> dict[str, Any]:
    if "[" in data:
        main, metadata = data.split("[", 1)
        metadata = "[" + metadata
    else:
        main = data
        metadata = ""
    main = main.strip()
    start, end = main.split("-", 1)
    connection: dict[str, Any] = {
        "start": start,
        "end": end,
    }
    connection.update(parse_metadata(metadata))
    return connection


def parse_config(file_path: Path) -> dict[str, list[str]]:
    """Parse a .txt formatted config file"""
    data: defaultdict[str, list[str]] = defaultdict(list)

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[key.strip()].append(value.strip())
    network: dict[str, Any] = {}
    if "nb_drones" in data:
        network["nb_drones"] = int(data["nb_drones"][0])
    if "start_hub" in data:
        network["start_hub"] = parse_hub(data["start_hub"][0])
    if "end_hub" in data:
        network["end_hub"] = parse_hub(data["end_hub"][0])
    if "hub" in data:
        network["hubs"] = [
            parse_hub(hub) for hub in data["hub"]
        ]
    if "connection" in data:
        network["connections"] = [
            parse_connection(connection) for connection in data["connection"]
        ]
    return network
