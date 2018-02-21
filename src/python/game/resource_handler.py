import pygame
from python.game.settings import RESOURCES, WINDOW_SIZE, SHIP_RESOURCES, SHIP_SIZE, BEAM_RESOURCES, BULLET_SIZE, \
    EXPLOSION_RESOURCES, EXPLOSION_SIZE, SOUND_RESOURCES


BACKGROUND_IMAGE = "bg"
PLAYER_SPRITE = "player"
ENEMY_SPRITE = "enemy"
BULLET_SPRITE = "bullet"
EXPLOSION_SPRITES_1 = "explosion_1"
EXPLOSION_SPRITES_2 = "explosion_2"
EXPLOSION_SOUND = "explosion"
ENEMY_SOUND = "enemy"
PLAYER_SOUND = "player"
BACKGROUND_MUSIC = SOUND_RESOURCES + "xeon6.ogg"


def load_image(root, path, size):
    return resize(pygame.image.load(root + path), size)


def resize(obj, size):
    return pygame.transform.scale(obj, size)


def load_images():
    return {
        BACKGROUND_IMAGE: load_image(RESOURCES, "space_bg.png", WINDOW_SIZE),
        PLAYER_SPRITE: load_image(SHIP_RESOURCES, "1B.png", SHIP_SIZE),
        ENEMY_SPRITE: load_image(SHIP_RESOURCES, "8B.png", SHIP_SIZE),
        BULLET_SPRITE: load_image(BEAM_RESOURCES, "B0.png", BULLET_SIZE),
        EXPLOSION_SPRITES_1: [
            load_image(EXPLOSION_RESOURCES, "ex1/e_0001.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0002.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0003.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0004.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0005.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0006.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0007.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0008.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0009.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0010.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0011.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0012.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0013.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0014.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex1/e_0015.png", EXPLOSION_SIZE)
        ],
        EXPLOSION_SPRITES_2: [
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0001.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0002.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0003.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0004.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0005.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0006.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0007.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0008.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0009.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0010.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0011.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0012.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0013.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0014.png", EXPLOSION_SIZE),
            load_image(EXPLOSION_RESOURCES, "ex2/k2_0015.png", EXPLOSION_SIZE)
        ]
    }


def load_sounds():
    player = pygame.mixer.Sound(SOUND_RESOURCES + "flaunch.wav")
    enemy = pygame.mixer.Sound(SOUND_RESOURCES + "slimeball.wav")
    explosion = pygame.mixer.Sound(SOUND_RESOURCES + "explosion.wav")
    player.set_volume(1)
    enemy.set_volume(0.1)
    explosion.set_volume(0.5)
    return {
        PLAYER_SOUND: player,
        ENEMY_SOUND: enemy,
        EXPLOSION_SOUND: explosion
    }
