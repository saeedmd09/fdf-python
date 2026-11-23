import math
import tkinter as tk

from fdf.model import Map, Point


class App:
    def __init__(self, map_data: Map) -> None:
        self.map = map_data
        self.zoom = 1.0

        self.root = tk.Tk()
        self.root.title("FdF - Wireframe Viewer")
        self.root.geometry("1000x700")
        self.root.minsize(400, 300)

        self.canvas = tk.Canvas(
            self.root,
            background="#202020",
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)

        self.root.bind("<Escape>", self._on_escape)
        self.root.bind("+", self._zoom_in)
        self.root.bind("-", self._zoom_out)
        self.root.bind("=", self._zoom_in)

    def run(self) -> None:
        self.root.mainloop()

    def _project(self) -> dict[tuple[int, int], tuple[float, float]]:
        angle = math.radians(30)
        projected: dict[tuple[int, int], tuple[float, float]] = {}

        for point in self.map:
            x = (point.x - point.y) * math.cos(angle)
            y = (point.x + point.y) * math.sin(angle) - point.z
            projected[(point.x, point.y)] = (x, y)

        return projected

    def _draw(self) -> None:
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1 or len(self.map) == 0:
            return

        projected = self._project()

        min_x = min(point[0] for point in projected.values())
        max_x = max(point[0] for point in projected.values())
        min_y = min(point[1] for point in projected.values())
        max_y = max(point[1] for point in projected.values())

        map_width = max(max_x - min_x, 1.0)
        map_height = max(max_y - min_y, 1.0)

        scale = min(width / map_width, height / map_height) * 0.9
        scale *= self.zoom

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        positions: dict[tuple[int, int], tuple[float, float]] = {}

        for key, (x, y) in projected.items():
            screen_x = (x - center_x) * scale + width / 2
            screen_y = (y - center_y) * scale + height / 2
            positions[key] = (screen_x, screen_y)

        for y in range(self.map.height):
            for x in range(self.map.width):
                point = self.map.points[y][x]
                x1, y1 = positions[(x, y)]
                line_color = point.color or "#FFFFFF"

                if x + 1 < self.map.width:
                    x2, y2 = positions[(x + 1, y)]
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=line_color,
                        width=2,
                    )

                if y + 1 < self.map.height:
                    x2, y2 = positions[(x, y + 1)]
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=line_color,
                        width=2,
                    )

    def _zoom_in(self, event: tk.Event) -> None:
        self.zoom = min(self.zoom * 1.2, 10.0)
        self._draw()

    def _zoom_out(self, event: tk.Event) -> None:
        self.zoom = max(self.zoom / 1.2, 0.1)
        self._draw()

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        if event.delta > 0:
            self.zoom = min(self.zoom * 1.1, 10.0)
        else:
            self.zoom = max(self.zoom / 1.1, 0.1)

        self._draw()

    def _on_resize(self, event: tk.Event) -> None:
        self.root.after_idle(self._draw)

    def _on_escape(self, event: tk.Event) -> None:
        self.root.destroy()