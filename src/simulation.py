from models import Network, Simulation, Drone
from renderer import render_turn, render_summary
from collections import Counter
from pathfinding import compute_distances_to_end, is_blocked, travel_turns


# def precompute_distance_to_goal(network: Network) -> dict[str, int]:
#     adjacency: dict[str, list[str]] = defaultdict(list)
#
#     for connection in network.connections:
#         a: str = connection.start.name
#         b: str = connection.end.name
#         adjacency[a].append(b)
#         adjacency[b].append(a)
#     distances = {network.end_hub.name: 0}
#     queue = deque([network.end_hub.name])
#     while queue:
#         current = queue.popleft()
#         for neighbor in adjacency[current]:
#             if neighbor not in distances:
#                 distances[neighbor] = distances[current] + 1
#                 queue.append(neighbor)
#     return distances


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
    distances = compute_distances_to_end(network)

    for drone in simulation.drones:
        network.start_hub.occupants.append(drone)
    render_turn(turn_counter, network)
    max_turns = max(100, (len(network.hubs) + 2) * network.nb_drones * 20)
    turn_counter = 1
    while len(network.end_hub.occupants) != network.nb_drones:
        if turn_counter > max_turns:
            raise RuntimeError(
                f"no progress after {max_turns} turns: check network for capacity deadlocks"
            )
        in_transit = [d for d in simulation.drones if d.in_transit]
        link_usage: Counter[int] = Counter(id(d.in_transit) for d in in_transit)
        moved_any: bool = False
        for drone in simulation.drones:
            if drone.current_hub == network.end_hub or drone.in_transit is not None:
                continue
            current_distance = distances.get(drone.current_hub.name)
            if current_distance is None:
                continue  # dead end: no route to the goal from here
            candidates = []
            for connection in network.connections:
                if connection.start is not drone.current_hub:
                    continue  # one-way: only the written direction counts
                next_hub = connection.end
                if is_blocked(next_hub):
                    continue
                next_distance = distances.get(next_hub.name)
                if next_distance is None or next_distance >= current_distance:
                    continue
                if next_hub.nb_occupants >= next_hub.metadata.get("max_drones", 1):
                    continue
                if link_usage[id(connection)] >= connection.metadata.get(
                    "max_link_capacity", 1
                ):
                    continue
                candidates.append((next_distance, next_hub.nb_occupants, connection))
            if not candidates:
                continue
            candidates.sort(key=lambda c: (c[0], c[1]))
            connection = candidates[0][2]
            next_hub = connection.end
            link_usage[id(connection)] += 1
            drone.current_hub.nb_occupants -= 1
            drone.current_hub.occupants.remove(drone)
            next_hub.nb_occupants += 1  # reserves the slot immediately
            if travel_turns(next_hub) == 1:
                next_hub.occupants.append(drone)
                drone.current_hub = next_hub
            else:  # restricted zone: takes one extra turn to land
                drone.in_transit = connection
                drone.arrival_turn = turn_counter + 1
            moved_any = True
        for drone in in_transit:
            if drone.arrival_turn == turn_counter:
                drone.in_transit.end.occupants.append(drone)
                drone.current_hub = drone.in_transit.end
                drone.in_transit = None
        render_turn(turn_counter, network)
        if not moved_any and not in_transit:
            raise RuntimeError(
                f"deadlock at turn {turn_counter}: no drone could move"
            )
        turn_counter += 1
    render_summary(network, turn_counter - 1)
