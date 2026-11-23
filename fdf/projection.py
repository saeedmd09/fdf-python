import math

from fdf.model import Map, Point


class Camera:
    def __init__(
        self,
        scale: float = 1.0,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
        z_scale: float = 1.0,
    ) -> None:
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.z_scale = z_scale

    def project(self, point: Point) -> tuple[float, float]:
        angle = math.radians(30)

        projected_x = (point.x - point.y) * math.cos(angle)
        projected_y = (
            (point.x + point.y) * math.sin(angle)
            - point.z * self.z_scale
        )

        screen_x = projected_x * self.scale + self.offset_x
        screen_y = projected_y * self.scale + self.offset_y

        return screen_x, screen_y

    def fit(self, map_data: Map, width: int, height: int) -> None:
        points = list(map_data)

        if not points or width <= 0 or height <= 0:
            return

        angle = math.radians(30)

        projected_points = []

        for point in points:
            x = (point.x - point.y) * math.cos(angle)
            y = (
                (point.x + point.y) * math.sin(angle)
                - point.z * self.z_scale
            )
            projected_points.append((x, y))

        min_x = min(point[0] for point in projected_points)
        max_x = max(point[0] for point in projected_points)
        min_y = min(point[1] for point in projected_points)
        max_y = max(point[1] for point in projected_points)

        map_width = max(max_x - min_x, 1.0)
        map_height = max(max_y - min_y, 1.0)

        self.scale = min(
            width / map_width,
            height / map_height,
        ) * 0.9

        self.offset_x = width / 2 - (
            (min_x + max_x) / 2
        ) * self.scale

        self.offset_y = height / 2 - (
            (min_y + max_y) / 2
        ) * self.scale