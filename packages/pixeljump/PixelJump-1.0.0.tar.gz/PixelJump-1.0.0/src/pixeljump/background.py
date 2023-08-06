from dataclasses import dataclass
import pygame


@dataclass(kw_only=True)
class Background:
    scaling: float
    pos: tuple[int, int]
    image: pygame.surface.Surface
