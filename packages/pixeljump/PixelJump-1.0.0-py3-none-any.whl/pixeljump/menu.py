import sys

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from pixeljump.assets import get_music, get_sprite_image, get_sprite_image_ck
from pixeljump.settings import load_settings
import pygame

settings = load_settings()

WINDOW_WIDTH = int(settings["window"]["screen_width"])
WINDOW_HEIGHT = int(settings["window"]["screen_height"])


def pause_screen():
    pause_image = get_sprite_image("pause", (WINDOW_WIDTH, WINDOW_HEIGHT))
    window = pygame.display.get_surface()
    pause_out_sound = get_music("pause_out.wav")
    slider_width, slider_height = int(WINDOW_WIDTH * 0.7), int(WINDOW_HEIGHT * 0.1)
    slider = Slider(
        window,
        window.get_width() // 2 - slider_width // 2,
        WINDOW_HEIGHT - 150,
        slider_width,
        slider_height,
        handleRadius=25,
        min=0.0,
        max=1.0,
        step=0.01,
        initial=pygame.mixer.music.get_volume(),
    )
    text_width, text_height = 100, 50
    text = TextBox(
        window,
        window.get_width() // 2 - text_width // 2,
        window.get_height() - 200,
        text_width,
        text_height,
    )
    text.disable()
    text.setText("music volume")
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_out_sound.play()
                    return
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_DOWN:
                    new_value = slider.getValue() - 0.1
                    if new_value < 0:
                        new_value = 0
                    slider.setValue(new_value)
                if event.key == pygame.K_UP:
                    new_value = slider.getValue() + 0.1
                    if new_value > 1.0:
                        new_value = 1.0
                    slider.setValue(new_value)
        pygame.mixer.music.set_volume(slider.getValue())
        window.fill(pygame.Color("white"))
        window.blit(pause_image, (0, 0))
        slider.draw()
        text.draw()
        pygame_widgets.update(events)
        pygame.display.update()


def show_menu() -> int:
    menu_image = get_sprite_image("menu", (WINDOW_WIDTH, WINDOW_HEIGHT))
    window = pygame.display.get_surface()
    menu_sound = get_music("menu_sound.wav")
    menu_music = get_music("100_victories.wav")
    menu_music.set_volume(0.2)

    menu_music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.Channel(1).play(menu_sound)
                menu_music.fadeout(1000)
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return 0
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3
        window.blit(menu_image, [0, 0])
        pygame.display.update()


def win_screen():
    window = pygame.display.get_surface()
    font = pygame.font.SysFont("arial", int(window.get_height() * 0.05))
    title = font.render(
        "YOU WIN! Press Enter to continue or Q to exit the game",
        True,
        pygame.Color("black"),
    )
    win_center = window.get_rect().center
    title_center = title.get_rect().center
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return

        window.fill(pygame.Color("yellow"))
        window.blit(
            title, (win_center[0] - title_center[0], win_center[1] - title_center[1])
        )
        pygame.display.update()


def win_screen1():
    window = pygame.display.get_surface()
    win_image = get_sprite_image("win_screen1", (WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return

        window.blit(
            win_image, (0,0)
        )
        pygame.display.update()


def win_screen2():
    window = pygame.display.get_surface()
    win_image = get_sprite_image("win_screen2", (WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return

        window.blit(
            win_image, (0,0)
        )
        pygame.display.update()


def win_screen3():
    window = pygame.display.get_surface()
    win_image = get_sprite_image_ck("win_screen3", (WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return

        window.blit(
            win_image, (0,0)
        )
        pygame.display.update()