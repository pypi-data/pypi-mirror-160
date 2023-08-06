import pygame
import random
from pixeljump.projectile import Projectile
from pixeljump.settings import load_settings
from pixeljump.assets import get_sprite_image, get_music
from pixeljump.animations import load_animation, change_action
from pixeljump.menu import pause_screen, win_screen1, win_screen2, win_screen3
from pixeljump.die import Fade
from pixeljump.particles import RocketParticles


settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]
PLAYER_COLOR = settings["colors"]["player"]
FPS = settings["window"]["fps"]
PLAYER_HORIZONTAL_VEL = settings["player"]["horizontal_velocity"]
PLAYER_VERTICAL_VEL = settings["player"]["vertical_velocity"]
GRAVITY = settings["player"]["gravity"]


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        position: tuple[int, int],
        *groups: pygame.sprite.Group,
        act: int,
        target: pygame.sprite.Sprite,
        collision_sprites: pygame.sprite.Group,
        visible_sprites: pygame.sprite.Group,
        active_sprites: pygame.sprite.Group,
        enemy_sprites: pygame.sprite.Group,
        can_shoot: bool = False
    ):
        super().__init__(*groups)
        self.health = 3
        self.heart_image = get_sprite_image("heart", (TILE_SIZE, TILE_SIZE))
        self.image = get_sprite_image("KNIGHT", (TILE_SIZE, TILE_SIZE), convert=False)
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = pygame.Vector2()
        self.enemy_sprites = enemy_sprites
        self.collision_sprites = collision_sprites
        self.visible_sprites = visible_sprites
        self.active_sprites = active_sprites
        self.target = target
        self.can_jump = True
        self.can_double_jump = True
        self.muted = False
        self.die = pygame.sprite.Group(Fade())
        self.dead = False
        self.orig_pos = position
        self.can_rocket = False
        self.rocket_timer = 70
        self.act = act
        self.rocket_acceleration = 0
        self.can_shoot = can_shoot

        # For animations
        self.animation_images: dict[str, pygame.Surface] = {}
        self.animation_database = {
            "idle": load_animation("idle", [7, 7, 40], self.animation_images),
            "running": load_animation(
                "running", [7, 7, 7, 7, 7, 7, 7, 7], self.animation_images
            ),
            "jumping": load_animation("jumping", [7], self.animation_images),
        }
        self.player_action = "idle"
        self.player_frame = 0
        self.player_flip = False

        # For audio
        self.jump_sound = get_music("jump.wav")
        self.step_sound = [
            get_music("step0.wav"),
            get_music("step1.wav"),
        ]
        self.step_sound_timer = 0
        self.step_sound[0].set_volume(0.5)
        self.step_sound[1].set_volume(0.5)

        self.death_music = get_music("ded.wav")
        self.death_music.set_volume(0.2)

        self.pause_in_sound = get_music("pause_in.wav")
        self.falling_sound = get_music("falling.wav")

        self.rocket_sound = get_music("rocket.wav")
        self.rocket_sound_timer = 10

        self.end_act = False

        self.got_hit_cd = 0

        self.gravity = GRAVITY

        self.shoot_sound = get_music("projectile_player.wav")

    def got_hit(self) -> bool:
        if self.got_hit_cd <= 0:
            self.health -= 1
            self.got_hit_cd = 2 * FPS
            return True
        return False

    def input(self):
        if self.dead:
            return

        if self.step_sound_timer > 0:
            self.step_sound_timer -= 1

        if self.rocket_sound_timer > 0:
            self.rocket_sound_timer -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity.x = -PLAYER_HORIZONTAL_VEL
        elif keys[pygame.K_d]:
            self.velocity.x = PLAYER_HORIZONTAL_VEL
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE]:
            if self.can_rocket and self.rocket_timer > 0:
                if self.rocket_sound_timer == 0:
                    self.rocket_sound.play()
                    self.rocket_sound_timer = 10
                self.rocket_acceleration -= 0.4
                self.velocity.y += self.rocket_acceleration
                if self.velocity.y < -10:
                    self.velocity.y = -10
                self.rocket_timer -= 1
                RocketParticles(
                    (self.rect.bottomleft[0] + 10, self.rect.bottomleft[1] - 10),
                    (random.randint(0, 20) / 10 - 2, random.randint(0, 20) / 10),
                    self.visible_sprites,
                    self.active_sprites,
                )

                RocketParticles(
                    (self.rect.bottomright[0] - 20, self.rect.bottomright[1] - 10),
                    (random.randint(0, 20) / 10, random.randint(0, 20) / 10),
                    self.visible_sprites,
                    self.active_sprites,
                )

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.can_jump:
                        self.velocity.y = -PLAYER_VERTICAL_VEL
                        self.can_jump = False
                        self.jump_sound.play()
                    elif self.can_double_jump:
                        self.velocity.y = -PLAYER_VERTICAL_VEL
                        self.can_double_jump = False
                        self.jump_sound.play()
                    elif (
                        not self.can_double_jump and not self.can_jump and self.act == 2
                    ):
                        self.can_rocket = True
                        self.rocket_acceleration = 0
                if event.key == pygame.K_ESCAPE:
                    self.pause_in_sound.play()
                    pause_screen()
                if event.key == pygame.K_m:
                    self.toggle_mute()
                if self.can_shoot and event.key == pygame.K_p:
                    self.shoot_sound.play()
                    if not self.player_flip:
                        Projectile(
                            (self.rect.centerx, self.rect.centery - 10),
                            self.visible_sprites,
                            self.active_sprites,
                            direction="left" if self.player_flip else "right",
                            collision_sprites=self.collision_sprites,
                            enemy_sprites=self.enemy_sprites,
                        )
                    else:
                        Projectile(
                            (self.rect.centerx - 64, self.rect.centery - 10),
                            self.visible_sprites,
                            self.active_sprites,
                            direction="left" if self.player_flip else "right",
                            collision_sprites=self.collision_sprites,
                            enemy_sprites=self.enemy_sprites,
                        )
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

    def toggle_mute(self) -> None:
        if not self.muted:
            self.step_sound[0].set_volume(0)
            self.step_sound[1].set_volume(0)
            self.jump_sound.set_volume(0)
            pygame.mixer.music.pause()
            self.muted = True
        else:
            self.step_sound[0].set_volume(0.5)
            self.step_sound[0].set_volume(0.5)
            self.jump_sound.set_volume(1)
            pygame.mixer.music.unpause()
            self.muted = False

    def check_win(self) -> None:
        assert self.target.rect is not None
        if self.rect.colliderect(self.target.rect):
            self.target.win_sound.play()
            self.end_act = True
            if self.act == 1:
                win_screen1()
            elif self.act == 2 and not self.can_shoot:
                win_screen2()
            elif self.act == 2 and self.can_shoot:
                win_screen3()

    def animation(self):
        if self.velocity.x > 0:
            self.player_action, self.player_frame = change_action(
                self.player_action, self.player_frame, "running"
            )
            self.player_flip = False

        if self.velocity.x == 0 and self.velocity.y == 0:
            self.player_action, self.player_frame = change_action(
                self.player_action, self.player_frame, "idle"
            )

        if self.velocity.x < 0:
            self.player_action, self.player_frame = change_action(
                self.player_action, self.player_frame, "running"
            )
            self.player_flip = True

        if self.can_rocket:
            self.player_action, self.player_frame = change_action(
                self.player_action, self.player_frame, "jumping"
            )

    def animating_image(self):
        self.player_frame += 1
        if self.player_frame >= len(self.animation_database[self.player_action]):
            self.player_frame = 0
        player_img_id = self.animation_database[self.player_action][self.player_frame]
        player_image = self.animation_images[player_img_id]
        self.image = pygame.transform.flip(player_image, self.player_flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if self.rect is not None and sprite.rect is not None:
                if sprite.rect.colliderect(self.rect):
                    if self.velocity.x < 0:
                        self.rect.left = sprite.rect.right
                    if self.velocity.x > 0:
                        self.rect.right = sprite.rect.left

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
                        self.can_jump = True
                        self.can_double_jump = True
                        self.can_rocket = False
                        self.rocket_timer = 70
                        self.rocket_acceleration = 0
                        if self.velocity.x != 0:
                            if self.step_sound_timer == 0:
                                self.step_sound_timer = 30
                                random.choice(self.step_sound).play()

    def apply_gravity(self):
        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

    def check_alive(self):
        if self.rect.y > pygame.display.get_window_size()[1] * 2:
            self.falling_sound.play()
            self.player_die()

    def player_die(self) -> None:
        curr = pygame.time.get_ticks()
        end = curr + (3 * 1000)
        self.dead = True
        self.velocity = pygame.Vector2((0, 0))
        window = pygame.display.get_surface()
        font = pygame.font.SysFont("comicsans", 50, bold=True)
        text = font.render("YOU DIED", True, pygame.Color("red"))
        pygame.mixer.music.stop()
        self.death_music.play()
        clock = pygame.time.Clock()
        while curr < end:
            self.die.update()
            self.die.draw(window)
            window.blit(
                text,
                (
                    window.get_width() // 2 - text.get_width() // 2,
                    window.get_height() // 2 - text.get_height() // 2,
                ),
            )
            curr = pygame.time.get_ticks()
            pygame.display.update()
            clock.tick(10)
        self.death_music.stop()
        self.kill()
        # self.dead = False
        # self.health = 3
        # self.rect.topleft = self.orig_pos
        # pygame.mixer.music.play()

    def draw_health(self) -> None:
        window = pygame.display.get_surface()
        for i in range(self.health):
            window.blit(
                self.heart_image,
                (window.get_width() - ((i + 1) * TILE_SIZE * 1.15), 10),
            )

    def update(self):
        self.input()
        self.animation()
        self.animating_image()
        self.rect.x += int(self.velocity.x)
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()
        # self.check_alive()
        self.check_win()
        if self.got_hit_cd > 0:
            self.got_hit_cd -= 1
        self.draw_health()
