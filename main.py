import sys

from fdf.app import App
from fdf.parser import FdfError, parse_map


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "Usage: python main.py <file.fdf>",
            file=sys.stderr,
        )
        return 2

    file_path = sys.argv[1]

    try:
        map_data = parse_map(file_path)
    except (FdfError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    app = App(map_data)
    app.run()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())