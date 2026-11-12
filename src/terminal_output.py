import sys
from matplotlib.colors import to_rgb
from models import Network, Hub, Simulation


def colored_label(hub: Hub) -> str:
    """Ensure that hub text colors in terminal match their metadata colors."""
    color_name = str(hub.metadata.get("color", "")).strip().lower()
    if not color_name or not sys.stdout.isatty():
        return hub.name
    try:
        r, g, b = (round(value * 255) for value in to_rgb(color_name))
    except ValueError:
        return hub.name
    return f"\x1b[38;2;{r};{g};{b}m{hub.name}\x1b[0m"


def print_turn(simulation: Simulation) -> None:
    """Print a compact, human-readable snapshot of the network state."""
    moves: list[str] = []
    for drone in simulation.drones:
        moves.append(f"D{drone.id}-{colored_label(drone.current_hub)}")
    print(" ".join(moves))
    print()


def print_summary(network: Network, turns_taken: int) -> None:
    """Print a short summary once every drone has reached the end hub."""
    print(
        f"\nAll {network.nb_drones} drone(s) reached "
        f"'{network.end_hub.name}' in {turns_taken} turn(s)."
    )
