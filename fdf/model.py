from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    z: int
    color: str | None = None


class Map:
    def __init__(self, points: list[list[Point]]) -> None:
        self.points = points
        self.height = len(points)
        self.width = len(points[0]) if points else 0

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self) -> Iterator[Point]:
        for row in self.points:
            yield from row

    def neighbors(self, point: Point) -> list[Point]:
        result: list[Point] = []
        x, y = point.x, point.y

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy

            if 0 <= ny < self.height and 0 <= nx < self.width:
                result.append(self.points[ny][nx])

        return result