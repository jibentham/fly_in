from models import Network, Simulation, Drone
from terminal_output import print_turn, print_summary
from collections import Counter
from pathfinding import compute_distances_to_end, is_blocked, travel_turns


class SimulationRunner:
    def __init__(self, network: Network):
        self.network = network
        self.simulation: Simulation = Simulation(
                drones=[
                            Drone(
                                id=i,
                                current_hub=network.start_hub,
                                ) for i in range(1, network.nb_drones + 1)
                        ]
                )
        self.turn = 0
        self.max_turns = max(100, (len(network.hubs) + 2) * network.nb_drones * 20)
        self.distances = compute_distances_to_end(network)
        network.start_hub.occupants.clear()
        network.start_hub.nb_occupants = network.nb_drones
        for drone in self.simulation.drones:
            network.start_hub.occupants.append(drone)
        self.finished = False
        self.failed = False

    def simulate_step(self) -> bool:
        network = self.network
        simulation = self.simulation
        distances = self.distances
        turn = self.turn + 1

        if turn > self.max_turns:
            self.failed = True
            raise RuntimeError(
                f"no progress after {self.max_turns} turns: check network for capacity deadlocks"
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
                drone.arrival_turn = turn + 1
            moved_any = True
        for drone in in_transit:
            if drone.arrival_turn == turn:
                drone.in_transit.end.occupants.append(drone)
                drone.current_hub = drone.in_transit.end
                drone.in_transit = None
        self.turn = turn
        self.finished = (len(network.end_hub.occupants) == network.nb_drones)
        if not moved_any and not in_transit:
            self.failed = True
            raise RuntimeError(
                f"deadlock at turn {turn}: no drone could move"
            )
        if self.failed:
            self.finished = True
        print_turn(turn, simulation)
        if self.finished:
            print_summary(network, turn)
        return not self.finished
