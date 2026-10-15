from models import Network, Hub, Drone, Simulation


def print_drone(drone: Drone) -> str:
    """ Display one hub as a compact 'name(occupants/capacity)' string."""
    if drone.in_transit is None:
        return f"Drone {drone.id}: located at {drone.current_hub.name}."
    elif drone.in_transit is not None:
        return f"Drone {drone.id}: in transit from {drone.in_transit.start.name} to {drone.in_transit.end.name}. Due for arrival at turn {drone.arrival_turn}."


def print_turn(turn: int, simulation: Simulation) -> None:
    """Print a compact, human-readable snapshot of the network state."""
    print(f"turn {turn:>3}:\n")
    for drone in simulation.drones:
        print(print_drone(drone))
    print("\n\n")


def print_summary(network: Network, turns_taken: int) -> None:
    """Print a short summary once every drone has reached the end hub."""
    print()
    print(
        f"All {network.nb_drones} drone(s) reached "
        f"'{network.end_hub.name}' in {turns_taken} turn(s)."
    )
