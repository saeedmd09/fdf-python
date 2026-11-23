import re
from pathlib import Path

from fdf.model import Map, Point


class FdfError(Exception):
    pass


class MapFormatError(FdfError):
    pass


def parse_map(file_path: str | Path) -> Map:
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        raise MapFormatError("The file is empty")

    points: list[list[Point]] = []
    expected_width: int | None = None

    for y, line in enumerate(lines):
        values = line.split()

        if not values:
            raise MapFormatError(f"Row {y + 1}: empty row")

        if expected_width is None:
            expected_width = len(values)
        elif len(values) != expected_width:
            raise MapFormatError(
                f"Row {y + 1}: inconsistent number of columns"
            )

        row: list[Point] = []

        for x, value in enumerate(values):
            parts = value.split(",")

            if len(parts) > 2:
                raise MapFormatError(
                    f"Row {y + 1}, column {x + 1}: invalid format"
                )

            try:
                z = int(parts[0])
            except ValueError:
                raise MapFormatError(
                    f"Row {y + 1}, column {x + 1}: invalid height"
                ) from None

            color = None

            if len(parts) == 2:
                if not re.fullmatch(
                    r"0x[0-9a-f]{1,6}",
                    parts[1],
                    re.IGNORECASE
                ):
                    raise MapFormatError(
                        f"Row {y + 1}, column {x + 1}: invalid color"
                    )

                color = f"#{int(parts[1], 16):06X}"

            row.append(
                Point(
                    x=x,
                    y=y,
                    z=z,
                    color=color
                )
            )

        points.append(row)

    return Map(points)