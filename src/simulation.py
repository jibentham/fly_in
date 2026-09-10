from models import Network, Simulation, Drone
from renderer import render_turn, render_summary


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
            for connection in network.connections:
                max_drones = connection.end.metadata.get("max_drones", 1)
                if (
                    connection.start == drone.current_hub
                    and connection.end.nb_occupants
                    < max_drones
                ):
                    connection.start.nb_occupants -= 1
                    connection.start.occupants.remove(drone)
                    connection.end.nb_occupants += 1
                    connection.end.occupants.append(drone)
                    drone.current_hub = connection.end
                    moved_any = True
                    break
        render_turn(turn_counter, network)
        if not moved_any:
            raise RuntimeError(
                f"deadlock at turn {turn_counter}: no drone could move"
            )
        turn_counter += 1
    render_summary(network, turn_counter - 1)
