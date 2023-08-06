import pygame
from pixeljump.assets import get_sprite_image, get_music
from pixeljump.animations import load_animation, change_action, load_particles
from pixeljump.eprojectile import EnemyProjectile


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(pygame.Color("black"))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites

        self.hit_sound = get_music("hit.wav")

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if self.rect is not None and sprite.rect is not None:
                if sprite.rect.colliderect(self.rect):
                    if self.velocity.x < 0:
                        self.rect.left = sprite.rect.right
                        self.velocity.x *= -1
                    elif self.velocity.x > 0:
                        self.rect.right = sprite.rect.left
                        self.velocity *= -1
        for sprite in self.enemy_collision_sprites.sprites():
            if self.rect is not None and sprite.rect is not None:
                if sprite.rect.colliderect(self.rect):
                    if self.velocity.x < 0:
                        self.rect.left = sprite.rect.right
                        self.velocity.x *= -1
                    elif self.velocity.x > 0:
                        self.rect.right = sprite.rect.left
                        self.velocity *= -1

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if self.rect is not None and sprite.rect is not None:
                if sprite.rect.colliderect(self.rect):
                    if self.velocity.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.velocity.y = 0
                    if self.velocity.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.velocity.y = 0

    def checkPlayer(self):
        if pygame.sprite.spritecollide(self, self.player_sprite, False, pygame.sprite.collide_mask):
            for player in self.player_sprite:
                assert player.rect is not None
                if player.got_hit():
                    self.hit_sound.play()
                if player.health <= 0:
                    player.player_die()

    def move(self) -> None:
        for player in self.player_sprite:
            if abs(player.rect.centerx - self.rect.centerx) < 200:
                if player.rect.left <= self.rect.centerx <= player.rect.right:
                    self.velocity.x = 0
                elif self.rect.centerx + 5 > player.rect.centerx:
                    self.velocity.x = -1 * self.speed
                elif self.rect.centerx - 5 < player.rect.centerx:
                    self.velocity.x = self.speed

    def update(self) -> None:
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        # self.move()
        self.checkPlayer()


class MushroomEnemy(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("mushroom", (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites

        self.hit_sound = get_music("hit1.wav")

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "walking": load_animation(
                "mushroom_walking",
                [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                self.animation_images,
            ),
            "idle": load_animation("mushroom_idle", [10], self.animation_images),
        }
        self.enemy_action = "idle"
        self.enemy_frame = 0
        self.enemy_flip = False

    def animation(self):
        if self.velocity.x > 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = False

        if self.velocity.x == 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "idle"
            )

        if self.velocity.x < 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = True

    def animating_image(self):
        self.enemy_frame += 1
        if self.enemy_frame >= len(self.animation_database[self.enemy_action]):
            self.enemy_frame = 0
        enemy_img_id = self.animation_database[self.enemy_action][self.enemy_frame]
        enemy_image = self.animation_images[enemy_img_id]
        self.image = pygame.transform.flip(enemy_image, self.enemy_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.move()
        self.checkPlayer()


class FroggyEnemy(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("froggy", (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites
        self.hit_sound = get_music("hit1.wav")

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "walking": load_animation(
                "froggy_walking", [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], self.animation_images
            ),
            "idle": load_animation("froggy_idle", [7, 7, 7, 7], self.animation_images),
        }
        self.enemy_action = "idle"
        self.enemy_frame = 0
        self.enemy_flip = True

    def animation(self):
        if self.velocity.x > 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = True

        if self.velocity.x == 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "idle"
            )

        if self.velocity.x < 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = False

    def animating_image(self):
        self.enemy_frame += 1
        if self.enemy_frame >= len(self.animation_database[self.enemy_action]):
            self.enemy_frame = 0
        enemy_img_id = self.animation_database[self.enemy_action][self.enemy_frame]
        enemy_image = self.animation_images[enemy_img_id]
        self.image = pygame.transform.flip(enemy_image, self.enemy_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.move()
        self.checkPlayer()


class Dragon(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("dragon", (192, 192))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites
        self.hit_sound = get_music("hit1.wav")

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "flying": load_particles(
                "dragon", [7, 7, 7, 7, 7, 7, 7, 7, 7], self.animation_images, (64 * 3, 64 * 3)
            )
        }
        self.enemy_action = "flying"
        self.enemy_frame = 0
        self.enemy_flip = True

    def animation(self):
        if self.velocity.x > 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "flying"
            )
            self.enemy_flip = True

        if self.velocity.x == 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "flying"
            )

        if self.velocity.x < 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "flying"
            )
            self.enemy_flip = False

    def animating_image(self):
        self.enemy_frame += 1
        if self.enemy_frame >= len(self.animation_database[self.enemy_action]):
            self.enemy_frame = 0
        enemy_img_id = self.animation_database[self.enemy_action][self.enemy_frame]
        enemy_image = self.animation_images[enemy_img_id]
        self.image = pygame.transform.flip(enemy_image, self.enemy_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self) -> None:
        for player in self.player_sprite:
            if abs(player.rect.centerx - self.rect.centerx) < 400 and abs(player.rect.centery - self.rect.centery) < 400:
                if player.rect.left <= self.rect.centerx <= player.rect.right:
                    self.velocity.x = 0
                elif self.rect.centerx + 5 > player.rect.centerx:
                    self.velocity.x = -1 * self.speed
                elif self.rect.centerx - 5 < player.rect.centerx:
                    self.velocity.x = self.speed
            if abs(player.rect.centery - self.rect.centery) < 400 and abs(player.rect.centerx - self.rect.centerx) < 400:
                if player.rect.top <= self.rect.centery <= player.rect.bottom:
                    self.velocity.y = 0
                elif self.rect.centery + 5 > player.rect.centery:
                    self.velocity.y = -1 * self.speed
                elif self.rect.centery - 5 < player.rect.centery:
                    self.velocity.y = self.speed
            else:
                self.velocity.y = 0

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.rect.y += int(self.velocity.y)
        self.vertical_collisions()
        self.move()
        self.checkPlayer()


class Nightmare(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("nightmare", (197, 128))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites
        self.hit_sound = get_music("hit1.wav")

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "walking": load_particles(
                "nightmare", [7, 7, 7, 7], self.animation_images, (197, 128)
            )
        }
        self.enemy_action = "walking"
        self.enemy_frame = 0
        self.enemy_flip = True

    def animation(self):
        if self.velocity.x > 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = True

        if self.velocity.x == 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )

        if self.velocity.x < 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = False

    def animating_image(self):
        self.enemy_frame += 1
        if self.enemy_frame >= len(self.animation_database[self.enemy_action]):
            self.enemy_frame = 0
        enemy_img_id = self.animation_database[self.enemy_action][self.enemy_frame]
        enemy_image = self.animation_images[enemy_img_id]
        self.image = pygame.transform.flip(enemy_image, self.enemy_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self) -> None:
        for player in self.player_sprite:
            if abs(player.rect.centerx - self.rect.centerx) < 200 and abs(player.rect.centery - self.rect.centery) < 200:
                if player.rect.left <= self.rect.centerx <= player.rect.right:
                    self.velocity.x = 0
                elif self.rect.centerx + 5 > player.rect.centerx:
                    self.velocity.x = -1 * self.speed
                elif self.rect.centerx - 5 < player.rect.centerx:
                    self.velocity.x = self.speed

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.move()
        self.checkPlayer()


class Border(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(pygame.Color("black"))
        self.speed = 0
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites
        self.hit_sound = get_music("falling.wav")

    def checkPlayer(self):
        for player in self.player_sprite:
            assert player.rect is not None
            if self.rect.colliderect(player.rect):
                self.hit_sound.play()
                player.player_die()

    def update(self) -> None:
        self.checkPlayer()


class Marine(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        visible_sprites: pygame.sprite.Group,
        active_sprites: pygame.sprite.Group,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("marine", (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.velocity = pygame.Vector2((self.speed, 0))
        self.visible_sprites = visible_sprites
        self.active_sprites = active_sprites
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites
        self.hit_sound = get_music("hit1.wav")
        self.shoot_sound = get_music("projectile_enemy.wav")
        self.death_sound = get_music("death_marine.wav")

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "walking": load_particles(
                "marine_running", [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], self.animation_images, (64, 64)
            ),
            "idle": load_particles("marine_idle", [7, 7, 7, 7], self.animation_images, (64, 64)),
        }
        self.enemy_action = "idle"
        self.enemy_frame = 0
        self.enemy_flip = False
        self.cooldown = 4

    def animation(self):
        if self.velocity.x > 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = False

        if self.velocity.x == 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "idle"
            )

        if self.velocity.x < 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = True

    def animating_image(self):
        self.enemy_frame += 1
        if self.enemy_frame >= len(self.animation_database[self.enemy_action]):
            self.enemy_frame = 0
        enemy_img_id = self.animation_database[self.enemy_action][self.enemy_frame]
        enemy_image = self.animation_images[enemy_img_id]
        self.image = pygame.transform.flip(enemy_image, self.enemy_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self) -> None:
        for player in self.player_sprite:
            if abs(player.rect.centerx - self.rect.centerx) < 800 and abs(player.rect.centery - self.rect.centery) < 400:
                if player.rect.left <= self.rect.centerx <= player.rect.right:
                    self.velocity.x = 0
                elif self.rect.centerx + 5 > player.rect.centerx:
                    self.velocity.x = -1 * self.speed
                elif self.rect.centerx - 5 < player.rect.centerx:
                    self.velocity.x = self.speed
            if abs(player.rect.centerx - self.rect.centerx) < 800 and abs(player.rect.centery - self.rect.centery) < 400:
                if player.rect.top - 5 <= self.rect.centery <= player.rect.bottom + 5:
                    self.cooldown -= 1
                    if self.cooldown == 0:
                        self.shoot_sound.play()
                        EnemyProjectile(
                            (self.rect.centerx, self.rect.centery - 20),
                            self.visible_sprites,
                            self.active_sprites,
                            direction="left" if self.enemy_flip else "right",
                            collision_sprites=self.collision_sprites,
                            player_sprite=self.player_sprite,
                        )
                        self.cooldown = 30

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.move()
        self.checkPlayer()


class Alien1(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("alien1", (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 7
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites
        self.hit_sound = get_music("hit1.wav")
        self.death_sound = get_music("death_alien1.wav")

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "flying": load_particles(
                "alien1_flying", [7, 7, 7, 7, 7, 7, 7, 7], self.animation_images, (64, 64)
            )
        }
        self.enemy_action = "flying"
        self.enemy_frame = 0
        self.enemy_flip = True

    def animation(self):
        if self.velocity.x > 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "flying"
            )
            self.enemy_flip = True

        if self.velocity.x == 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "flying"
            )

        if self.velocity.x < 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "flying"
            )
            self.enemy_flip = False

    def animating_image(self):
        self.enemy_frame += 1
        if self.enemy_frame >= len(self.animation_database[self.enemy_action]):
            self.enemy_frame = 0
        enemy_img_id = self.animation_database[self.enemy_action][self.enemy_frame]
        enemy_image = self.animation_images[enemy_img_id]
        self.image = pygame.transform.flip(enemy_image, self.enemy_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self) -> None:
        for player in self.player_sprite:
            if abs(player.rect.centerx - self.rect.centerx) < 600 and abs(player.rect.centery - self.rect.centery) < 600:
                if player.rect.left <= self.rect.centerx <= player.rect.right:
                    self.velocity.x = 0
                elif self.rect.centerx + 5 > player.rect.centerx:
                    self.velocity.x = -1 * self.speed
                elif self.rect.centerx - 5 < player.rect.centerx:
                    self.velocity.x = self.speed
            if abs(player.rect.centery - self.rect.centery) < 600 and abs(player.rect.centerx - self.rect.centerx) < 600:
                if player.rect.top + 10 <= self.rect.centery <= player.rect.bottom - 10:
                    self.velocity.y = 0
                elif self.rect.centery + 5 > player.rect.centery:
                    self.velocity.y = -1 * self.speed
                elif self.rect.centery - 5 < player.rect.centery:
                    self.velocity.y = self.speed
            else:
                self.velocity.y = 0

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.rect.y += int(self.velocity.y)
        self.vertical_collisions()
        self.move()
        self.checkPlayer()


class Alien2(Enemy):
    def __init__(
        self,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup,
        collision_sprites: pygame.sprite.Group,
        enemy_collision_sprites: pygame.sprite.Group,
        player_sprite: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            pos,
            *groups,
            collision_sprites=collision_sprites,
            enemy_collision_sprites=enemy_collision_sprites,
            player_sprite=player_sprite,
        )
        self.image = get_sprite_image("alien2", (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8
        self.velocity = pygame.Vector2((self.speed, 0))
        self.collision_sprites = collision_sprites
        self.player_sprite = player_sprite
        self.enemy_collision_sprites = enemy_collision_sprites
        self.hit_sound = get_music("hit1.wav")
        self.death_sound = get_music("death_alien2.wav")

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "walking": load_particles(
                "alien2_walking", [7, 7, 7, 7, 7, 7], self.animation_images, (64, 64)
            ),
            "idle": load_particles(
                "alien2_idle", [7, 7, 7, 7], self.animation_images, (64, 64)
            )
        }
        self.enemy_action = "walking"
        self.enemy_frame = 0
        self.enemy_flip = True

    def animation(self):
        if self.velocity.x > 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = True

        if self.velocity.x == 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "idle"
            )

        if self.velocity.x < 0:
            self.enemy_action, self.enemy_frame = change_action(
                self.enemy_action, self.enemy_frame, "walking"
            )
            self.enemy_flip = False

    def animating_image(self):
        self.enemy_frame += 1
        if self.enemy_frame >= len(self.animation_database[self.enemy_action]):
            self.enemy_frame = 0
        enemy_img_id = self.animation_database[self.enemy_action][self.enemy_frame]
        enemy_image = self.animation_images[enemy_img_id]
        self.image = pygame.transform.flip(enemy_image, self.enemy_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self) -> None:
        for player in self.player_sprite:
            if abs(player.rect.centerx - self.rect.centerx) < 800 and abs(player.rect.centery - self.rect.centery) < 400:
                if player.rect.left <= self.rect.centerx <= player.rect.right:
                    self.velocity.x = 0
                elif self.rect.centerx + 5 > player.rect.centerx:
                    self.velocity.x = -1 * self.speed
                elif self.rect.centerx - 5 < player.rect.centerx:
                    self.velocity.x = self.speed

    def update(self) -> None:
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.move()
        self.checkPlayer()
