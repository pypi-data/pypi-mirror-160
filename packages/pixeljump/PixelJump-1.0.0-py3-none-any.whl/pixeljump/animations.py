from pixeljump.assets import get_animation_image, get_animation_image_black
from pixeljump.settings import load_settings

settings = load_settings()

TILE_SIZE = settings["window"]["tile_size"]


# Eg. frame_duration is [7,7] (list of multiple frame durations), frame
def load_animation(animation_name: str, frame_duration, animation_images) -> list[str]:
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + "_" + str(n)
        animation_image = get_animation_image(
            animation_frame_id, animation_name, (TILE_SIZE, TILE_SIZE), True
        )
        animation_images[animation_frame_id] = animation_image.copy()
        for _ in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def load_particles(animation_name: str, frame_duration, animation_images, scale: tuple) -> list[str]:
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + "_" + str(n)
        animation_image = get_animation_image(
            animation_frame_id, animation_name, scale, True
        )
        animation_images[animation_frame_id] = animation_image.copy()
        for _ in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def load_projectile(animation_name: str, frame_duration, animation_images, scale: tuple) -> list[str]:
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + "_" + str(n)
        animation_image = get_animation_image_black(
            animation_frame_id, animation_name, scale, True
        )
        animation_images[animation_frame_id] = animation_image.copy()
        for _ in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_action):
    if action_var != new_action:
        action_var = new_action
        frame = 0
    return action_var, frame


def load_animation_3x(animation_name: str, frame_duration, animation_images) -> list[str]:
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + "_" + str(n)
        animation_image = get_animation_image(
            animation_frame_id, animation_name, (TILE_SIZE * 3, TILE_SIZE * 3), True
        )
        animation_images[animation_frame_id] = animation_image.copy()
        for _ in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data
