import pygame
from typing import Literal
from pixeljump.settings import load_settings
from pixeljump.animations import load_projectile, change_action
from pixeljump.assets import get_music

settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]


class EnemyProjectile(pygame.sprite.Sprite):

    horizontal_velocity = 20

    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        direction: Literal["right", "left"],
        collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((63, 32))
        self.image.set_alpha(0)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.direction: int = 1 if direction == "right" else -1
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite

        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "shooting": load_projectile(
                "projectile", [7, 7, 7, 7, 7], self.animation_images, (63, 32)
            )
        }
        self.projectile_action = "shooting"
        self.projectile_frame = 0
        self.projectile_flip: bool = False if self.direction == 1 else True
        self.hit_sound = get_music("damage_gun.wav")

    def animation(self):
        if self.horizontal_velocity * self.direction > 0:
            self.projectile_action, self.projectile_frame = change_action(
                self.projectile_action, self.projectile_frame, "shooting"
            )
            self.projectile_flip = False

        if self.horizontal_velocity * self.direction < 0:
            self.projectile_action, self.projectile_frame = change_action(
                self.projectile_action, self.projectile_frame, "shooting"
            )
            self.projectile_flip = True

    def animating_image(self):
        self.projectile_frame += 1
        if self.projectile_frame >= len(self.animation_database[self.projectile_action]):
            self.projectile_frame = 0
        proj_img_id = self.animation_database[self.projectile_action][self.projectile_frame]
        proj_image = self.animation_images[proj_img_id]
        self.image = pygame.transform.flip(proj_image, self.projectile_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self) -> None:
        self.rect.x += self.horizontal_velocity * self.direction

    def check_collision(self) -> None:
        for sprite in self.collision_sprites:
            assert sprite.rect is not None
            if self.rect.colliderect(sprite.rect):
                self.kill()
        if pygame.sprite.spritecollide(self, self.player_sprite, False, pygame.sprite.collide_mask):
            for player in self.player_sprite:
                assert player.rect is not None
                if player.got_hit():
                    self.hit_sound.play()
                if player.health <= 0:
                    player.player_die()

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.move()
        self.check_collision()