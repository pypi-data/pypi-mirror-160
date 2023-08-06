import pygame
from pixeljump.player import Player
from pixeljump.settings import load_settings
from pixeljump.background import Background

settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]
WINDOW_WIDTH = settings["window"]["screen_width"]
WINDOW_HEIGHT = settings["window"]["screen_height"]


class Camera(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.offset: pygame.Vector2 = pygame.Vector2(0, 0)

    def draw(
        self,
        surface: pygame.surface.Surface,
        backgrounds: list[Background],
        clock: pygame.time.Clock,
    ) -> None:
        for background in backgrounds:
            surface.blit(
                background.image,
                (
                    background.pos[0] - self.offset.x * background.scaling,
                    background.pos[1] - self.offset.y * background.scaling,
                ),
            )
        for sprite in self:
            if sprite.rect is not None and sprite.image is not None:
                sprite_topleft = pygame.Vector2(sprite.rect.topleft)
                surface.blit(sprite.image, sprite_topleft - self.offset)
        font_size = int(pygame.display.get_surface().get_width() * 0.03)
        font = pygame.font.SysFont("Arial", font_size, True)
        text = font.render(f"FPS: {clock.get_fps():.2f}", True, pygame.Color("red"))
        surface.blit(text, (0, 0))

    def update_player_pos(self, player: Player) -> None:
        if player.rect is not None:
            self.offset.x += (
                (player.rect.x - self.offset.x) - (WINDOW_WIDTH // 2 + TILE_SIZE // 2)
            ) // 20

            self.offset.y += (
                (player.rect.y - self.offset.y) - (WINDOW_HEIGHT // 2 + TILE_SIZE // 2)
            ) // 20
