from models import Network, Simulation, Drone
from renderer import render_turn, render_summary
from collections import defaultdict, deque


def precompute_distance_to_goal(network: Network) -> dict[str, int]:
    adjacency: dict[str, list[str]] = defaultdict(list)

    for connection in network.connections:
        a: str = connection.start.name
        b: str = connection.end.name
        adjacency[a].append(b)
        adjacency[b].append(a)
    distances = {network.end_hub.name: 0}
    queue = deque([network.end_hub.name])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances


def simulate(network: Network) -> None:
    simulation: Simulation = Simulation(
            drones=[
                        Drone(
                            id=i,
                            current_hub=network.start_hub,
                            ) for i in range(1, network.nb_drones + 1)
                    ]
            )
    turn_counter: int = 0
    network.start_hub.nb_occupants = network.nb_drones
    distances = precompute_distance_to_goal(network)

    for drone in simulation.drones:
        network.start_hub.occupants.append(drone)
    render_turn(turn_counter, network)
    max_turns = max(100, (len(network.hubs) + 2) * network.nb_drones * 20)
    turn_counter = 1
    while network.end_hub.nb_occupants != network.nb_drones:
        if turn_counter > max_turns:
            raise RuntimeError(
                f"no progress after {max_turns} turns: check network for capacity deadlocks"
            )
        moved_any: bool = False
        for drone in simulation.drones:
            if drone.current_hub == network.end_hub:
                continue
            current_distance = distances[drone.current_hub.name]
            valid_connections = []
            for connection in network.connections:
                if connection.start == drone.current_hub:
                    next_hub = connection.end
                elif connection.end == drone.current_hub:
                    next_hub = connection.start
                else:
                    continue
                if distances[next_hub.name] >= current_distance:
                    continue
                max_drones = next_hub.metadata.get("max_drones", 1)
                if next_hub.nb_occupants >= max_drones:
                    continue
                valid_connections.append(next_hub)
            if not valid_connections:
                continue
            next_hub = min(valid_connections, key=lambda hub: distances[hub.name])
            drone.current_hub.nb_occupants -= 1
            drone.current_hub.occupants.remove(drone)
            next_hub.nb_occupants += 1
            next_hub.occupants.append(drone)
            drone.current_hub = next_hub
            moved_any = True
        render_turn(turn_counter, network)
        if not moved_any:
            raise RuntimeError(
                f"deadlock at turn {turn_counter}: no drone could move"
            )
        turn_counter += 1
    render_summary(network, turn_counter - 1)
