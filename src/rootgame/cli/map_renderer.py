from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple, Optional
from shared.shared_types import ClearingInfo


# ----------------------------
# Layout helpers
# ----------------------------

def scale_positions(
    positions: Dict[int, Tuple[int, int]],
    sx: int = 2,
    sy: int = 2,
    ox: int = 0,
    oy: int = 0,
) -> Dict[int, Tuple[int, int]]:
    """Scale and offset top-left node coordinates (keeps your originals intact)."""
    return {k: (ox + x * sx, oy + y * sy) for k, (x, y) in positions.items()}


def compute_canvas_size(
    positions: Dict[int, Tuple[int, int]],
    node_w: int,
    node_h: int,
    margin: int = 4,
) -> Tuple[int, int]:
    """Compute a canvas size that fits all nodes plus a margin."""
    max_x = max(x for x, _ in positions.values())
    max_y = max(y for _, y in positions.values())
    return (max_x + node_w + margin, max_y + node_h + margin)


# ----------------------------
# ASCII Renderer
# ----------------------------

class AsciiBoardRenderer:
    """
    Multi-line node cards + cleaner edges (border-to-border, diagonal-capable),
    with improved rectangle-line intersection so edges hit the box neatly.
    """

    NODE_W = 17
    NODE_H = 7

    def __init__(
        self,
        width: int,
        height: int,
        positions: Dict[int, Tuple[int, int]],   # node_id -> (x, y) top-left of node
        edges: Iterable[Tuple[int, int]],
    ) -> None:
        self.width = width
        self.height = height
        self.positions = positions
        self.edges = {self._norm_edge(a, b) for a, b in edges}

    def render(self, info_by_clearing: Dict[int, ClearingInfo]) -> str:
        canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # 1) edges first
        for a, b in sorted(self.edges):
            self._draw_edge(canvas, a, b)

        # 2) nodes second (nodes overwrite edge artifacts inside their boxes)
        for node_id, (x, y) in self.positions.items():
            info = info_by_clearing.get(node_id, ClearingInfo())
            lines = self._format_node_lines(node_id, info)
            self._draw_node(canvas, x, y, lines)

        return "\n".join("".join(row).rstrip() for row in canvas).rstrip()

    # ---------------- Node formatting ----------------

    def _format_node_lines(self, node_id: int, info: ClearingInfo) -> List[str]:
        inner_w = self.NODE_W - 2

        suit = (info.suit or "").upper()
        header = f"{node_id:02d} {suit}".strip()

        # Warriors: "W: C2 E1"
        w_parts = [f"{k}{v}" for k, v in sorted(info.warriors.items()) if v]
        warriors_line = "W: " + (" ".join(w_parts) if w_parts else "-")

        # Tiles/buildings: "B: roost,sawmill"
        tiles_line = "B: " + (",".join(info.tiles) if info.tiles else "-")

        # Tokens: "T: sympathy(1) keep(1)"
        tok_bits: List[str] = []
        for name, items in sorted(info.tokens.items()):
            cnt = len(items)
            if cnt:
                tok_bits.append(f"{name}({cnt})")
        tokens_line = "T: " + (" ".join(tok_bits) if tok_bits else "-")

        extra_line = ""  # free slot for later

        def pad(s: str) -> str:
            return s[:inner_w].ljust(inner_w)

        top = "." + "-" * inner_w + "."
        bottom = "'" + "-" * inner_w + "'"

        return [
            top,
            "|" + pad(header) + "|",
            "|" + pad(warriors_line) + "|",
            "|" + pad(tiles_line) + "|",
            "|" + pad(tokens_line) + "|",
            "|" + pad(extra_line) + "|",
            bottom,
        ]

    def _draw_node(self, canvas: List[List[str]], x: int, y: int, lines: List[str]) -> None:
        if x < 0 or y < 0:
            return
        if x + self.NODE_W > self.width or y + self.NODE_H > self.height:
            return
        for dy, line in enumerate(lines):
            for dx, ch in enumerate(line):
                canvas[y + dy][x + dx] = ch

    # ---------------- Edges ----------------

    def _draw_edge(self, canvas: List[List[str]], a: int, b: int) -> None:
        a_rect = self._node_rect(a)
        b_rect = self._node_rect(b)

        acx, acy = self._rect_center(a_rect)
        bcx, bcy = self._rect_center(b_rect)

        start = self._rect_line_intersection(a_rect, (acx, acy), (bcx, bcy))
        end = self._rect_line_intersection(b_rect, (bcx, bcy), (acx, acy))
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

    def _rect_line_intersection(
        self,
        rect: Tuple[int, int, int, int],
        p_inside: Tuple[int, int],
        p_towards: Tuple[int, int],
    ) -> Optional[Tuple[int, int]]:
        """
        True rectangle-line intersection from p_inside toward p_towards.
        Returns an (x,y) integer point on the rectangle boundary.

        Uses parametric ray and finds the earliest boundary hit (t > 0),
        then rounds to nearest integer boundary point.
        """
        x0, y0, x1, y1 = rect
        cx, cy = p_inside
        tx, ty = p_towards
        dx = tx - cx
        dy = ty - cy
        if dx == 0 and dy == 0:
            return None

        candidates: List[Tuple[float, float, float]] = []  # (t, x, y)

        # Intersect with vertical sides x=x0 and x=x1
        if dx != 0:
            for x_side in (x0, x1):
                t = (x_side - cx) / dx
                if t > 0:
                    y = cy + t * dy
                    if y0 <= y <= y1:
                        candidates.append((t, float(x_side), float(y)))

        # Intersect with horizontal sides y=y0 and y=y1
        if dy != 0:
            for y_side in (y0, y1):
                t = (y_side - cy) / dy
                if t > 0:
                    x = cx + t * dx
                    if x0 <= x <= x1:
                        candidates.append((t, float(x), float(y_side)))

        if not candidates:
            return None

        # Pick closest hit
        t, xf, yf = min(candidates, key=lambda c: c[0])

        # Round to int grid
        xi = int(round(xf))
        yi = int(round(yf))

        # Clamp to rect to be safe
        xi = min(max(xi, x0), x1)
        yi = min(max(yi, y0), y1)

        # Ensure it's on boundary; if rounding pushed inside, snap to nearest boundary
        if xi not in (x0, x1) and yi not in (y0, y1):
            # Snap to the boundary that was actually hit (based on which side was exact)
            # Prefer matching the float boundary if very close
            if abs(xf - x0) < 1e-6 or abs(xf - x1) < 1e-6:
                xi = x0 if abs(xf - x0) < abs(xf - x1) else x1
            elif abs(yf - y0) < 1e-6 or abs(yf - y1) < 1e-6:
                yi = y0 if abs(yf - y0) < abs(yf - y1) else y1
            else:
                # fallback: push to nearest side
                dist_left = abs(xi - x0)
                dist_right = abs(x1 - xi)
                dist_top = abs(yi - y0)
                dist_bot = abs(y1 - yi)
                m = min(dist_left, dist_right, dist_top, dist_bot)
                if m == dist_left:
                    xi = x0
                elif m == dist_right:
                    xi = x1
                elif m == dist_top:
                    yi = y0
                else:
                    yi = y1

        return (xi, yi)

    def _bresenham_with_chars(self, x0: int, y0: int, x1: int, y1: int):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        x, y = x0, y0
        prev = (x, y)
        while True:
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
        if step_x == 0 and step_y == 0:
            return " "
        if step_y == 0:
            return "-"
        if step_x == 0:
            return "|"
        # diagonal
        if (step_x > 0 and step_y > 0) or (step_x < 0 and step_y < 0):
            return "\\"
        return "/"

    def _merge_edge_char(self, canvas: List[List[str]], x: int, y: int, ch: str) -> None:
        if ch == " ":
            return
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        cur = canvas[y][x]

        # Avoid mutating node borders during edge drawing. Nodes will be drawn after anyway.
        if cur in (".", "'", "|", "-"):
            return

        if cur == " ":
            canvas[y][x] = ch
            return

        if cur == ch:
            return

        canvas[y][x] = "+"

    @staticmethod
    def _norm_edge(a: int, b: int) -> Tuple[int, int]:
        return (a, b) if a <= b else (b, a)


# ----------------------------
# DO NOT DROP: Your originals
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


# ----------------------------
# Recommended: scaled layout for more spacing
# ----------------------------

# Keep POSITIONS untouched; use scaled positions when rendering.
SCALED_POSITIONS = scale_positions(POSITIONS, sx=2, sy=2, ox=2, oy=1)


def make_renderer() -> AsciiBoardRenderer:
    w, h = compute_canvas_size(SCALED_POSITIONS, node_w=AsciiBoardRenderer.NODE_W, node_h=AsciiBoardRenderer.NODE_H, margin=6)
    return AsciiBoardRenderer(width=w, height=h, positions=SCALED_POSITIONS, edges=EDGES)


# ----------------------------
# Quick demo
# ----------------------------

if __name__ == "__main__":
    renderer = make_renderer()

    # Example game state snapshot (fill from your engine)
    state: Dict[int, ClearingInfo] = {
        3: ClearingInfo(suit="fox", warriors={"C": 2, "E": 1}, tiles=["roost"], tokens={"sympathy": ["s1"]}),
        5: ClearingInfo(suit="mouse", warriors={"C": 1}, tiles=["sawmill", "workshop"], tokens={}),
        10: ClearingInfo(suit="rabbit", warriors={"M": 3}, tiles=["base"], tokens={"tunnel": ["t1", "t2"]}),
    }

    print(renderer.render(state))