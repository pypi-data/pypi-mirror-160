import pygame


class Fade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.alpha = 0
        self.direction = 2

    def update(self):
        self.image.fill((0, 0, 0, self.alpha))
        if self.alpha < 255 - self.direction:
            self.alpha += self.direction
