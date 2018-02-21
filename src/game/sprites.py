import random
import pygame
import math
from pygame.sprite import Sprite
from settings import PLAYER_DEFAULT_SPEED, PLAYER_DEFAULT_POSITION, ENEMY_DEFAULT_SPEED, \
    PLAYER_BULLET_SPEED, ENEMY_BULLET_SPEED, WINDOW_SIZE, SHIP_SIZE, FPS


class Drawable(Sprite):
    def __init__(self, texture, position):
        super().__init__()
        self.image = texture
        self.rect = texture.get_rect(topleft=position)

    def _move(self, speed):
        self.rect = self.rect.move(speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Drawable):

    def __init__(self, texture):
        super().__init__(texture, PLAYER_DEFAULT_POSITION)
        self.__speed = PLAYER_DEFAULT_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left > 0 + self.__speed[0]:
                self._move((self.__speed[0] * -1, self.__speed[1]))
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right < WINDOW_SIZE[0] - self.__speed[0]:
                self._move(self.__speed)


class Enemy(Drawable):
    def norm(self, x): return 0

    def __init__(self, texture, position, inverted_direction, base_speed):
        super().__init__(texture, position)
        self.__speed = ENEMY_DEFAULT_SPEED
        self.set_speed(base_speed)
        self.__direction = 1 if not inverted_direction else -1
        rand = random.randint(1, 3)
        fun = None
        if rand == 1:
            fun = math.sin
        elif rand == 2:
            fun = math.cos
        else:
            fun = self.norm
        self.y_speed = fun

    def set_speed(self, speed):
        self.__speed = (ENEMY_DEFAULT_SPEED[0]*speed, ENEMY_DEFAULT_SPEED[1]*speed)

    def update(self):
        self._move((self.__speed[0] * self.__direction,
                    self.y_speed(math.radians(self.__speed[1]))*2))
        if self.rect.left < 0 + self.__speed[0] \
                or \
                self.rect.right > WINDOW_SIZE[0] - self.__speed[0]:
            self.__direction *= -1
        self.__speed = (self.__speed[0], (self.__speed[1] + 360 / FPS / 2) % 360)


class Bullet(Drawable):

    def __init__(self, texture, position, speed):
        super().__init__(texture, position)
        self.__speed = speed

    def update(self):
        self._move(self.__speed)
        if self.rect.top > WINDOW_SIZE[1] or self.rect.bottom < 0:
            self.kill()


class PlayerBullet(Bullet):
    def __init__(self, texture, position):
        super().__init__(texture, position, PLAYER_BULLET_SPEED)

    def update(self, enemies, on_hit):
        super().update()
        hits = pygame.sprite.spritecollide(self, enemies, True)
        if len(hits) > 0:
            self.kill()
            on_hit(hits)


class EnemyBullet(Bullet):
    def __init__(self, texture, position):
        super().__init__(texture, position, ENEMY_BULLET_SPEED)

    def update(self, player, player_hit):
        super().update()
        if player is not None and pygame.sprite.collide_rect(self, player):
            self.kill()
            player_hit()


class Animation(Drawable):
    def __init__(self, images, position, length):
        self.images = images
        self.image_index = 0
        self.time = 0
        self.limit = length / len(images)
        super().__init__(self.images[self.image_index], position)

    def update(self):
        super().update()
        self.time += 1 / FPS
        if self.time > self.limit:
            self.time = 0
            self.image_index += 1
            if self.image_index == len(self.images):
                self.kill()
            else:
                self.next_image()

    def next_image(self):
        self.image = self.images[self.image_index]
