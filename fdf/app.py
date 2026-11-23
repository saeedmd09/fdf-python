import math
import tkinter as tk

from fdf.model import Map


class App:
    def __init__(self, map_data: Map) -> None:
        self.map = map_data

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
        self.root.bind("<Escape>", self._on_escape)

    def run(self) -> None:
        self.root.mainloop()

    def _draw(self) -> None:
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1 or len(self.map) == 0:
            return

        angle = math.radians(30)
        projected: list[tuple[int, int, float, float]] = []

        for point in self.map:
            x = (point.x - point.y) * math.cos(angle)
            y = (
                (point.x + point.y) * math.sin(angle)
                - point.z
            )
            projected.append((point.x, point.y, x, y))

        min_x = min(item[2] for item in projected)
        max_x = max(item[2] for item in projected)
        min_y = min(item[3] for item in projected)
        max_y = max(item[3] for item in projected)

        map_width = max(max_x - min_x, 1.0)
        map_height = max(max_y - min_y, 1.0)

        scale = min(
            width / map_width,
            height / map_height,
        ) * 0.9

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        positions: dict[tuple[int, int], tuple[float, float]] = {}

        for x, y, projected_x, projected_y in projected:
            screen_x = (
                (projected_x - center_x) * scale + width / 2
            )
            screen_y = (
                (projected_y - center_y) * scale + height / 2
            )
            positions[(x, y)] = (screen_x, screen_y)

        for y in range(self.map.height):
            for x in range(self.map.width):
                x1, y1 = positions[(x, y)]

                if x + 1 < self.map.width:
                    x2, y2 = positions[(x + 1, y)]
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill="#FFFFFF",
                        width=2,
                    )

                if y + 1 < self.map.height:
                    x2, y2 = positions[(x, y + 1)]
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill="#FFFFFF",
                        width=2,
                    )

    def _on_resize(self, event: tk.Event[tk.Misc]) -> None:
        self.root.after_idle(self._draw)

    def _on_escape(self, event: tk.Event[tk.Misc]) -> None:
        self.root.destroy()