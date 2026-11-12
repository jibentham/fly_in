import heapq
from collections import defaultdict
from models import Network, Hub


def zone_type(hub: Hub) -> str:
    """Return the value of a zone's 'type' key."""
    return str(hub.metadata.get("zone"))


def is_blocked(hub: Hub) -> bool:
    """Check whether a zone's type is listed as 'blocked'."""
    return zone_type(hub) == "blocked"


def travel_turns(hub: Hub) -> int:
    """Return the number of turns it takes to enter a zone."""
    return 2 if zone_type(hub) == "restricted" else 1


def entry_cost(hub: Hub) -> tuple[int, int]:
    """Set the priority of different travel routes
     by determining a movement cost hierarchy."""
    return (travel_turns(hub), 0 if zone_type(hub) == "priority" else 1)


def compute_distances_to_end(network: Network) -> dict[str, tuple[int, int]]:
    """Utilize Dijkstra's algorithm to check the distance from the goal
     of each zone for efficient pathfinding"""
    by_name = {
        hub.name: hub for hub in [
            network.start_hub, network.end_hub, *network.hubs
            ]
    }
    predecessors: dict[str, list[Hub]] = defaultdict(list)
    distances: dict[str, tuple[int, int]] = {network.end_hub.name: (0, 0)}
    heap: list[tuple[tuple[int, int], str]] = [((0, 0), network.end_hub.name)]

    for connection in network.connections:
        if is_blocked(connection.start) or is_blocked(connection.end):
            continue
        predecessors[connection.end.name].append(connection.start)
    while heap:
        distance, name = heapq.heappop(heap)
        if distance > distances[name]:
            continue
        step = entry_cost(by_name[name])
        for predecessor in predecessors[name]:
            frontier = (distance[0] + step[0], distance[1] + step[1])
            if predecessor.name not in distances or (
                    frontier < distances[predecessor.name]
                    ):
                distances[predecessor.name] = frontier
                heapq.heappush(heap, (frontier, predecessor.name))
    return distances
