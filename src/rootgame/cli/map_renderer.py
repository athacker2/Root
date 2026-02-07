from __future__ import annotations
from typing import Dict, Iterable, List, Tuple


class AsciiBoardRenderer:
    """
    Renders a node+edge graph onto an ASCII canvas.

    Node box (7x3):
        .-----.
        |05 hi|
        '-----'

    Edges:
      - Connect from *border-to-border* of node boxes (not center-to-center)
      - Uses '-', '|', '/', '\\' for diagonals
      - Merges crossings with '+'
    """
    NODE_W = 7
    NODE_H = 3

    def __init__(
        self,
        width: int,
        height: int,
        positions: Dict[int, Tuple[int, int]],   # node_id -> (x, y) top-left
        edges: Iterable[Tuple[int, int]],
    ) -> None:
        self.width = width
        self.height = height
        self.positions = positions
        self.edges = {self._norm_edge(a, b) for a, b in edges}

    def render(self, notes: Dict[int, str]) -> str:
        canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # 1) edges first
        for a, b in sorted(self.edges):
            self._draw_edge(canvas, a, b)

        # 2) nodes second (overwrite any edge artifacts inside the box)
        for node_id, (x, y) in self.positions.items():
            note = notes.get(node_id, "")
            self._draw_node(canvas, node_id, x, y, note)

        return "\n".join("".join(row).rstrip() for row in canvas).rstrip()

    # ---------------- internals ----------------

    def _draw_node(self, canvas: List[List[str]], node_id: int, x: int, y: int, note: str) -> None:
        if not self._in_bounds(x, y) or not self._in_bounds(x + self.NODE_W - 1, y + self.NODE_H - 1):
            return

        # Top
        self._put(canvas, x + 0, y + 0, ".")
        for i in range(1, self.NODE_W - 1):
            self._put(canvas, x + i, y + 0, "-")
        self._put(canvas, x + self.NODE_W - 1, y + 0, ".")

        # Middle: |05 abc|
        self._put(canvas, x + 0, y + 1, "|")
        label = f"{node_id:02d}"
        inside = f"{label} {note}".ljust(self.NODE_W - 2)[: self.NODE_W - 2]
        for i, ch in enumerate(inside):
            self._put(canvas, x + 1 + i, y + 1, ch)
        self._put(canvas, x + self.NODE_W - 1, y + 1, "|")

        # Bottom
        self._put(canvas, x + 0, y + 2, "'")
        for i in range(1, self.NODE_W - 1):
            self._put(canvas, x + i, y + 2, "-")
        self._put(canvas, x + self.NODE_W - 1, y + 2, "'")

    def _draw_edge(self, canvas: List[List[str]], a: int, b: int) -> None:
        a_rect = self._node_rect(a)
        b_rect = self._node_rect(b)

        acx, acy = self._rect_center(a_rect)
        bcx, bcy = self._rect_center(b_rect)

        # border-to-border endpoints
        start = self._line_rect_intersection_exit(a_rect, (acx, acy), (bcx, bcy))
        end = self._line_rect_intersection_exit(b_rect, (bcx, bcy), (acx, acy))

        if start is None or end is None:
            return

        x0, y0 = start
        x1, y1 = end

        for x, y, ch in self._bresenham_with_chars(x0, y0, x1, y1):
            self._merge_edge_char(canvas, x, y, ch)

    def _node_rect(self, node_id: int) -> Tuple[int, int, int, int]:
        x, y = self.positions[node_id]
        # inclusive bounds
        return (x, y, x + self.NODE_W - 1, y + self.NODE_H - 1)

    @staticmethod
    def _rect_center(rect: Tuple[int, int, int, int]) -> Tuple[int, int]:
        x0, y0, x1, y1 = rect
        return ((x0 + x1) // 2, (y0 + y1) // 2)

    def _line_rect_intersection_exit(
        self,
        rect: Tuple[int, int, int, int],
        p_inside: Tuple[int, int],
        p_towards: Tuple[int, int],
    ) -> Tuple[int, int] | None:
        """
        Given a rectangle and a point inside it, find the first point *outside* the rect
        along the ray from p_inside toward p_towards, but return the last point that is
        still on the border (i.e., the exit point on the rectangle boundary).
        """
        x0, y0, x1, y1 = rect
        cx, cy = p_inside
        tx, ty = p_towards
        dx = tx - cx
        dy = ty - cy
        if dx == 0 and dy == 0:
            return None

        # Step outward with a normalized-ish direction (sign only for stepping).
        stepx = 0 if dx == 0 else (1 if dx > 0 else -1)
        stepy = 0 if dy == 0 else (1 if dy > 0 else -1)

        # Walk from center until we would leave; keep the last in-rect point as exit.
        x, y = cx, cy
        last_in = (x, y)
        # Hard cap so we never infinite loop
        for _ in range(500):
            nx, ny = x + stepx, y + stepy
            if x0 <= nx <= x1 and y0 <= ny <= y1:
                x, y = nx, ny
                last_in = (x, y)
            else:
                break

        # last_in is still inside; we want the border point (which it is).
        # But ensure it's actually on border.
        lx, ly = last_in
        if lx in (x0, x1) or ly in (y0, y1):
            return last_in

        # If for some reason we didn't land on border (rare with tiny boxes), clamp.
        lx = min(max(lx, x0), x1)
        ly = min(max(ly, y0), y1)
        return (lx, ly)

    def _bresenham_with_chars(self, x0: int, y0: int, x1: int, y1: int):
        """
        Bresenham line; yields (x,y,ch) where ch depends on local direction.
        """
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        x, y = x0, y0
        prev = (x, y)
        while True:
            # pick char based on step from prev -> (x,y)
            px, py = prev
            step_x = x - px
            step_y = y - py
            ch = self._step_char(step_x, step_y)

            yield x, y, ch

            if x == x1 and y == y1:
                break

            prev = (x, y)
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    @staticmethod
    def _step_char(step_x: int, step_y: int) -> str:
        # first point has (0,0) step
        if step_x == 0 and step_y == 0:
            return " "
        if step_y == 0:
            return "-"
        if step_x == 0:
            return "|"
        # diagonal
        # (x+, y+) or (x-, y-) => '\'
        # (x+, y-) or (x-, y+) => '/'
        if (step_x > 0 and step_y > 0) or (step_x < 0 and step_y < 0):
            return "\\"
        return "/"

    def _merge_edge_char(self, canvas: List[List[str]], x: int, y: int, ch: str) -> None:
        if ch == " ":
            return
        if not self._in_bounds(x, y):
            return

        cur = canvas[y][x]

        # Don't scribble over node box characters; nodes are drawn later anyway,
        # but this helps keep borders cleaner during edge pass.
        if cur in (".", "'", "|", "-"):
            return

        if cur == " ":
            canvas[y][x] = ch
            return

        # Merge crossings / overlaps
        if cur == ch:
            return
        canvas[y][x] = "+"

    def _put(self, canvas: List[List[str]], x: int, y: int, ch: str) -> None:
        if self._in_bounds(x, y):
            canvas[y][x] = ch

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    @staticmethod
    def _norm_edge(a: int, b: int) -> Tuple[int, int]:
        return (a, b) if a <= b else (b, a)


# ----------------------------
# Example layout (tweaked a bit)
# ----------------------------

POSITIONS: Dict[int, Tuple[int, int]] = {
    0: (4, 1),
    1: (40, 1),
    2: (72, 4),
    3: (36, 8),
    4: (6, 11),
    5: (28, 14),
    6: (54, 13),
    7: (74, 15),
    8: (8, 23),
    9: (30, 25),
    10: (52, 22),
    11: (74, 25),
}

EDGES = [
    (0,1), (0, 4), (0, 3),
    (1, 2),
    (2, 3), (2, 7),
    (3, 5),
    (4, 5), (4, 8),
    (5, 8), (5, 10), (5, 6),
    (6, 7), (6, 11),
    (7, 11),
    (8, 9),
    (9, 10),
    (10, 11),
]