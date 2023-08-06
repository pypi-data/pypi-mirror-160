import pygame

from pixeljump.level import Level
from pixeljump.background import Background
from pixeljump.enemies import Marine, Border, Alien1, Alien2
from pixeljump.tile import Tile3, EnemyTile
from pixeljump.player import Player
from pixeljump.settings import load_settings
from pixeljump.assets import (
    select_background_act,
    get_map,
    get_assets_path,
    select_background_act_sprite,
)
from pixeljump.spikes import Spike, CeilingSpike
from pixeljump.camera import Camera
from pixeljump.target import Target2

settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]
WINDOW_WIDTH = settings["window"]["screen_width"]
WINDOW_HEIGHT = settings["window"]["screen_height"]

get_background = select_background_act(3)
get_background_sprite = select_background_act_sprite(3)


class ActThree(Level):
    def __init__(self):
        self.player: Player
        self.window = pygame.display.get_surface()
        self.map = get_map("map3")
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
        self.play_bgm(get_assets_path() + "music/exploration.wav")
        self.setup_level()
        self.main_background = get_background("space_background")
        self.backgrounds = [
            Background(
                scaling=0.25,
                pos=(0, 0),
                image=get_background("far_stars", scale=(2, 1)),
            ),
            Background(
                scaling=0.35,
                pos=(0, 500),
                image=get_background("far_planet", scale=(2, 1)),
            ),
            Background(
                scaling=0.50,
                pos=(700, 1200),
                image=get_background_sprite("closer_planet", scale=(102 * 4, 230 * 4)),
            ),
            Background(
                scaling=0.75,
                pos=(1900, 1000),
                image=get_background_sprite("close_planet", scale=(176 * 4, 174 * 4)),
            ),
            Background(
                scaling=0.50,
                pos=(4500, 1500),
                image=get_background_sprite("closer_planet", scale=(102 * 4, 230 * 4)),
            ),
            Background(
                scaling=0.75,
                pos=(5100, 1500),
                image=get_background_sprite("close_planet", scale=(176 * 4, 174 * 4))
            ),
        ]

    def setup_level(self):
        p_x = 0
        p_y = 0
        for row_idx, row in enumerate(self.map):
            for col_idx, col in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if col == "P":
                    p_x = x
                    p_y = y

                if col == "M":
                    Marine(
                        (x, y),
                        self.enemy_sprites,
                        self.visible_sprites,
                        visible_sprites=self.visible_sprites,
                        active_sprites=self.active_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col == "A":
                    Alien1(
                        (x, y),
                        self.enemy_sprites,
                        self.visible_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col == "a":
                    Alien2(
                        (x, y),
                        self.enemy_sprites,
                        self.visible_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col == "I":
                    EnemyTile((x, y), self.enemy_collision_sprites)

                if col == "S":
                    Spike(
                        (x, y + 30),
                        self.enemy_sprites,
                        self.visible_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col == "s":
                    CeilingSpike(
                        (x, y - 10),
                        self.enemy_sprites,
                        self.visible_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col == "$":
                    self.target = Target2((x, y), self.visible_sprites)

                if col == "Z":
                    Border(
                        (x, y),
                        self.enemy_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col.isnumeric():
                    Tile3(
                        (x, y),
                        self.visible_sprites,
                        self.collision_sprites,
                        col=int(col),
                    )
        self.player = Player(
            (p_x, p_y),
            self.visible_sprites,
            self.active_sprites,
            self.player_sprite,
            target=self.target,
            act=2,
            collision_sprites=self.collision_sprites,
            visible_sprites=self.visible_sprites,
            active_sprites=self.active_sprites,
            enemy_sprites=self.enemy_sprites,
            can_shoot=True,
        )
        self.player.gravity = 0.5

    def play_bgm(self, path: str) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
