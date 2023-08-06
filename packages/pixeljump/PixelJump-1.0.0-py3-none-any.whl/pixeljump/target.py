import pygame
from pixeljump.settings import load_settings
from pixeljump.assets import get_sprite_image, get_music

settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]


class Target(pygame.sprite.Sprite):
    def __init__(
        self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup
    ) -> None:
        super().__init__(*groups)
        # self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = get_sprite_image("shoe", (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.win_sound = get_music("end_level.wav")


class Target1(pygame.sprite.Sprite):
    def __init__(
        self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup
    ) -> None:
        super().__init__(*groups)
        # self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = get_sprite_image("gun", (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.win_sound = get_music("end_level.wav")


class Target2(pygame.sprite.Sprite):
    def __init__(
        self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup
    ) -> None:
        super().__init__(*groups)
        # self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = get_sprite_image("princess", (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.win_sound = get_music("end_level.wav")