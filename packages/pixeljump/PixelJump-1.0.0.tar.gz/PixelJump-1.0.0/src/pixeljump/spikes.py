import pygame
from pixeljump.enemies import Enemy
from pixeljump.assets import get_sprite_image


class Spike(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("spikes1", (64, 42))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def checkPlayer(self):
        if pygame.sprite.spritecollide(
            self, self.player_sprite, False, pygame.sprite.collide_mask
        ):
            for player in self.player_sprite:
                assert player.rect is not None
                if player.got_hit():
                    self.hit_sound.play()
                if player.health <= 0:
                    player.player_die()

    def update(self):
        self.checkPlayer()


class CeilingSpike(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("spikes1", (64, 42))
        self.image = pygame.transform.flip(self.image, False, True)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def checkPlayer(self):
        if pygame.sprite.spritecollide(
            self, self.player_sprite, False, pygame.sprite.collide_mask
        ):
            for player in self.player_sprite:
                assert player.rect is not None
                if player.got_hit():
                    self.hit_sound.play()
                if player.health <= 0:
                    player.player_die()

    def update(self):
        self.checkPlayer()
