import pygame

from pixeljump.level import Level
from pixeljump.background import Background
from pixeljump.enemies import MushroomEnemy, FroggyEnemy
from pixeljump.tile import Tile, EnemyTile, TreeTile, PropTile
from pixeljump.player import Player
from pixeljump.settings import load_settings
from pixeljump.assets import select_background_act, get_map, get_assets_path
from pixeljump.spikes import Spike
from pixeljump.target import Target

settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]
WINDOW_WIDTH = settings["window"]["screen_width"]
WINDOW_HEIGHT = settings["window"]["screen_height"]

get_background = select_background_act(1)


class ActOne(Level):
    def __init__(self):
        super().__init__()
        self.play_bgm(get_assets_path() + "music/music.wav")
        self.main_background = get_background("parallax-mountain-bg")
        self.backgrounds = [
            Background(
                scaling=0.15,
                pos=(100, 100),
                image=get_background("far", scale=(1, 1)),
            ),
            Background(
                scaling=0.25,
                pos=(300, 100),
                image=get_background("close", scale=(2, 1)),
            ),
            Background(
                scaling=0.50,
                pos=(50, 100),
                image=get_background("trees", scale=(2, 1)),
            ),
            Background(
                scaling=0.75,
                pos=(250, 250),
                image=get_background("foreground", scale=(2, 1)),
            ),
        ]

    def setup_level(self):
        p_x = 0
        p_y = 0
        for row_idx, row in enumerate(get_map("map")):
            for col_idx, col in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if col == "P":
                    p_x = x
                    p_y = y
                if col == "E":
                    MushroomEnemy(
                        (x, y),
                        self.enemy_sprites,
                        self.visible_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )
                if col == "F":
                    FroggyEnemy(
                        (x, y),
                        self.enemy_sprites,
                        self.visible_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col == "I":
                    EnemyTile((x, y), self.enemy_collision_sprites)
                if col == "T":
                    TreeTile((x, y), self.visible_sprites)

                if col == "S":
                    Spike(
                        (x, y + 30),
                        self.enemy_sprites,
                        self.visible_sprites,
                        collision_sprites=self.collision_sprites,
                        enemy_collision_sprites=self.enemy_collision_sprites,
                        player_sprite=self.player_sprite,
                    )

                if col == "$":
                    self.target = Target((x, y), self.visible_sprites)

                if col == "#":
                    PropTile((x, y), self.visible_sprites)

                if col.isnumeric():
                    Tile(
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
            act=1,
            collision_sprites=self.collision_sprites,
            visible_sprites=self.visible_sprites,
            active_sprites=self.active_sprites,
            enemy_sprites=self.enemy_sprites,
            can_shoot=False,
        )

    def play_bgm(self, path: str) -> None:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
