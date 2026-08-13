from pathlib import Path
from parser import parse_config


def main() -> None:
    parent_directory: Path = Path(__file__).resolve().parent.parent

    for file in parent_directory.glob("*.txt"):
        data: dict[str, list[str]] = parse_config(file)
        print(f"\n{file.name}")
        print(data)


if __name__ == "__main__":
    main()

