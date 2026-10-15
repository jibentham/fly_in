from pathlib import Path
from parser import parse_config
from models import Network
from simulation import SimulationRunner
# from renderer_context import render_network


def main() -> None:
    source_directory: Path = Path(__file__).resolve().parent
    map_directory: Path = source_directory.parent/"maps"

    for directory in sorted(map_directory.iterdir()):
        if not directory.is_dir():
            continue
        for file in sorted(directory.glob("*.txt")):
            network: Network = parse_config(file)
            print("\n------------------------------------------------")
            print(f"\n{file.name}\n")
            network_sim = SimulationRunner(network)
            while network_sim.finished is False:
                network_sim.simulate_step()
            # render_network()
    print()


if __name__ == "__main__":
    main()
