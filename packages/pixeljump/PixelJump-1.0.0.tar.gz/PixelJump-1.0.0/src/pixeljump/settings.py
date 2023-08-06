import json
from pathlib import Path

root_dir = Path(__file__).parent.resolve()
SETTINGS_PATH = root_dir / "settings"

SETTINGS = {}


def load_settings() -> dict:
    global SETTINGS
    if not SETTINGS:
        import pygame

        with open(SETTINGS_PATH / "settings.json", "r") as f:
            settings = json.load(f)
            desktop_info = pygame.display.Info()
            desktop_width, desktop_height = (
                desktop_info.current_w,
                desktop_info.current_h,
            )
            width, height = int(desktop_width * 0.85), int(desktop_height * 0.85)
            settings["window"]["screen_width"] = width
            settings["window"]["screen_height"] = height
            SETTINGS = settings
            return SETTINGS
    return SETTINGS
