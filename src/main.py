from pathlib import Path
from parser import parse_config


def main() -> None:
    source_directory: Path = Path(__file__).resolve().parent
    map_directory: Path = source_directory.parent/"maps"

    for directory in map_directory.iterdir():
        if not directory.is_dir():
            continue
        for file in directory.glob("*.txt"):
            data: dict[str, list[str]] = parse_config(file)
            print("\n------------------------------------------------")
            print(f"\n{file.name}\n")
            print(data)
    print()


if __name__ == "__main__":
    main()
