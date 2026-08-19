from pathlib import Path
from collections import defaultdict
from typing import Any
from models import Hub, Connection, Network


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


def parse_hub(data: str) -> Hub:
    if "[" in data:
        main, metadata = data.split("[", 1)
        metadata = "[" + metadata
    else:
        main = data
        metadata = ""
    values = main.split()
    return Hub(
        name=values[0],
        x=int(values[1]),
        y=int(values[2]),
        metadata=parse_metadata(metadata),
        nb_occupants=0,
        )


def parse_connection(
    data: str,
    hubs: list[Hub],
    start_hub: Hub,
    end_hub: Hub,
) -> Connection:
    if "[" in data:
        main, metadata = data.split("[", 1)
        metadata = "[" + metadata
    else:
        main = data
        metadata = ""

    main = main.strip()

    if main.startswith("connection:"):
        main = main[len("connection:"):].strip()

    start_name, end_name = (x.strip() for x in main.split("-", 1))

    all_hubs = hubs + [start_hub, end_hub]
    hub_by_name = {hub.name: hub for hub in all_hubs}

    start = hub_by_name[start_name]
    end = hub_by_name[end_name]

    return Connection(
        start=start,
        end=end,
        metadata=parse_metadata(metadata),
    )


def parse_config(file_path: Path) -> Network:
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

    if "nb_drones" in data:
        nb_drones = int(data["nb_drones"][0])
    if "start_hub" in data:
        start_hub = parse_hub(data["start_hub"][0])
        start_hub.metadata["max_drones"] = nb_drones
    if "end_hub" in data:
        end_hub = parse_hub(data["end_hub"][0])
        end_hub.metadata["max_drones"] = nb_drones
    if "hub" in data:
        hubs = [
            parse_hub(hub) for hub in data["hub"]
        ]
    if "connection" in data:
        connections = [
            parse_connection(connection, hubs, start_hub, end_hub)
            for connection in data["connection"]
        ]
    return Network(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            hubs=hubs,
            connections=connections,
            )
