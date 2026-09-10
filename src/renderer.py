from models import Network


def render_hub(hub) -> str:
    """ Display one hub as a compact 'name(occupants/capacity)' string."""
    capacity = hub.metadata.get("max_drones")
    occupant_ids = ",".join(str(d.id) for d in hub.occupants)
    if capacity is not None:
        return f"{hub.name}[{occupant_ids}]({hub.nb_occupants}/{capacity})"
    return f"{hub.name}[{occupant_ids}]({hub.nb_occupants})"


def render_turn(turn: int, network: Network) -> None:
    """Print a compact, human-readable snapshot of the network state."""
    hubs = [network.start_hub, *network.hubs, network.end_hub]
    line = "  ".join(render_hub(hub) for hub in hubs)
    print(f"turn {turn:>3}: {line}")


def render_summary(network: Network, turns_taken: int) -> None:
    """Print a short summary once every drone has reached the end hub."""
    print()
    print(
        f"All {network.nb_drones} drone(s) reached "
        f"'{network.end_hub.name}' in {turns_taken} turn(s)."
    )
