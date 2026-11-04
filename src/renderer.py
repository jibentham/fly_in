from __future__ import annotations
import colorsys
import math
import sys
from collections import defaultdict
import pygame
from models import Hub, Network

BASE_W, BASE_H = 1200, 800
W, H = BASE_W, BASE_H
MX, MY, SS = 120, 90, 2
TURN_SECONDS, MAX_DT = 0.8, 1 / 30
REWIND = -1.0 / TURN_SECONDS  # playback time starts negative: a 1 s pause
BG, INK = (64, 64, 64), (226, 232, 242)
ZONES = {"normal": (190, 200, 215), "priority": (115, 205, 145),
         "restricted": (235, 165, 95), "blocked": (195, 105, 115)}
LINE_COLOR = (135, 145, 160)
DRONE_COLOR = (100, 190, 235)
DRONE_TEXT_COLOR = (245, 245, 245)
NEAREST = sorted((complex(i, j) for i in range(-12, 13)
                  for j in range(-12, 13)), key=abs)  # cells, nearest first


def all_hubs(net: Network) -> list[Hub]:
    return [net.start_hub, *net.hubs, net.end_hub]


def window_size(net: Network) -> tuple[int, int]:
    xs = [hub.x for hub in all_hubs(net)]
    ys = [hub.y for hub in all_hubs(net)]

    PIXELS_PER_X = 40
    PIXELS_PER_Y = 60

    wanted_w = max(
        BASE_W,
        math.ceil((max(xs) - min(xs)) * PIXELS_PER_X + 2 * MX),
    )
    wanted_h = max(
        BASE_H,
        math.ceil((max(ys) - min(ys)) * PIXELS_PER_Y + 2 * MY),
    )

    info = pygame.display.Info()
    max_w = max(BASE_W, (info.current_w or 1920) - 80)
    max_h = max(BASE_H, (info.current_h or 1080) - 120)

    return min(wanted_w, max_w), min(wanted_h, max_h)


def zone_of(hub: Hub) -> str:
    return str(hub.metadata.get("zone", "normal"))


def harmonize_color(
    color: pygame.Color,
    reference: tuple[int, ...],
    strength: float = 0.35,
) -> tuple[int, int, int]:
    """Blend a metadata colour towards its zone palette colour."""
    return tuple(
        round(c * (1 - strength) + r * strength)
        for c, r in zip(color[:3], reference)

