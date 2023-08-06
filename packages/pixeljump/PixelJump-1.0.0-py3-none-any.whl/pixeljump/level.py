import pygame
from abc import ABC, abstractmethod

from pixeljump.player import Player
from pixeljump.camera import Camera
from pixeljump.background import Background

from pixeljump.settings import load_settings

settings = load_settings()

FPS = settings["window"]["fps"]


class Level(ABC):
    def __init__(self):
        self.player: Player
        self.window = pygame.display.get_surface()
        # Updated every frame
        self.active_sprites = pygame.sprite.Group()
        # Drawn every frame
        self.visible_sprites = Camera()
        # Checks for collision every frame
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_collision_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.particle_sprites = pygame.sprite.Group()
        self.setup_level()
        self.main_background: pygame.surface.Surface
        self.backgrounds: list[Background]

    @abstractmethod
    def setup_level(self):
        pass

    def play_bgm(self, path: str) -> None:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    def run(self) -> bool:
        clock = pygame.time.Clock()
        while True:
            self.window.blit(self.main_background, (0, 0))
            self.visible_sprites.draw(self.window, self.backgrounds, clock)
            self.visible_sprites.update_player_pos(self.player)
            self.active_sprites.update()
            self.enemy_sprites.update()
            pygame.display.update()
            clock.tick(FPS)
            if self.player.end_act:
                return True
            if self.player.dead:
                return False
