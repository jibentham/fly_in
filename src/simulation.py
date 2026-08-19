from models import Network, Simulation, Drone


def simulate(network: Network) -> None:
    simulation: Simulation = Simulation(
            drones = [
                        Drone(
                            id=i,
                            current_hub=network.start_hub,
                            ) for i in range(1, network.nb_drones + 1)
                    ]
            )
    turn_counter: int = 0
    network.start_hub.occupants_nb = network.nb_drones

    for drone in simulation.drones:
        network.start_hub.occupants.append(drone)
    for connection in network.connections:
        for drone in simulation.drones:
            if connection.start == drone.current_hub and connection.end.occupants_nb < connection.end.metadata["max_drones"]:
                connection.start.occupants_nb -= 1
                connection.start.occupants.remove(drone)
                connection.end.occupants_nb += 1
                connection.end.occupants.append(drone)
        turn_counter += 1
        print(turn_counter)
        print()
        print(network)
