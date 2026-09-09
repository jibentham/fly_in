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
        if "=" not in tag:
            raise ValueError(
                f"Bad metadata {tag!r}: expected 'key=value'"
            )
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
    if len(values) < 3:
        raise ValueError(
            f"Bad hub definition {data!r}: expected 'name x y [metadata]'"
        )
    try:
        x = int(values[1])
        y = int(values[2])
    except ValueError as e:
        raise ValueError(
            f"Hub xy coordinates must be integers in {data!r}"
        ) from e
    return Hub(
        name=values[0],
        x=x,
        y=y,
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
    if "-" not in main:
        raise ValueError(
            f"Bad connection definition {data!r}: expected 'start-end'"
        )

    start_name, end_name = (x.strip() for x in main.split("-", 1))

    all_hubs = hubs + [start_hub, end_hub]
    hub_by_name = {hub.name: hub for hub in all_hubs}
    if start_name not in hub_by_name:
        raise ValueError(
            f"Connection references unknown hub {start_name!r}"
        )
    if end_name not in hub_by_name:
        raise ValueError(
            f"Connection references unknown hub {end_name!r}"
        )
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

    for key in ("nb_drones", "start_hub", "end_hub", "connection"):
        if key not in data:
            raise ValueError(
                f"Missing required entry '{key}' in config file {file_path.name}"
            )

    try:
        nb_drones = int(data["nb_drones"][0])
    except ValueError as e:
        raise ValueError(
            f"'nb_drones' must be an integer in config file {file_path.name}"
        )
    if nb_drones <= 0:
        raise ValueError(
            f"'nb_drones' must be positive in config file {file_path.name}"
        )
    start_hub = parse_hub(data["start_hub"][0])
    start_hub.metadata["max_drones"] = nb_drones
    end_hub = parse_hub(data["end_hub"][0])
    end_hub.metadata["max_drones"] = nb_drones
    hubs = [
        parse_hub(hub) for hub in data["hub"]
    ]
    hub_names = [start_hub.name, end_hub.name] + [hub.name for hub in hubs]
    if len(hub_names) != len(set(hub_names)):
        raise ValueError(
            f"Duplicate hub names found in config file {file_path.name}"
        )
    connections = [
        parse_connection(connection, hubs, start_hub, end_hub)
        for connection in data["connection"]
    ]
    network = Network(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            hubs=hubs,
            connections=connections,
            )
    _check_reachable(network, file_path)
    return network


def _check_reachable(network: Network, file_path: Path) -> None:
    """Ensure end_hub is reachable from start_hub, fail fast otherwise."""
    visited = {network.start_hub.name}
    frontier = [network.start_hub]
    adjacency: dict[str, list[Any]] = defaultdict(list)
    for connection in network.connections:
        adjacency[connection.start.name].append(connection.end)
 
    while frontier:
        current = frontier.pop()
        for neighbor in adjacency[current.name]:
            if neighbor.name not in visited:
                visited.add(neighbor.name)
                frontier.append(neighbor)
 
    if network.end_hub.name not in visited:
        raise ValueError(
            f"end_hub '{network.end_hub.name}' is not "
            "reachable from start_hub in config file {file_path.name}"
        )
