import random
import sys
import pygame
import math
from settings import RESOURCES, WINDOW_SIZE, SHIP_RESOURCES, SHIP_SIZE, PLAYER_DEFAULT_POSITION, BEAM_RESOURCES, BULLET_SIZE, \
    CAPTION, FPS, FONT_COLOR, EXPLOSION_RESOURCES, EXPLOSION_SIZE, SOUND_RESOURCES, PLAYER_BULLET_SPEED, ENEMY_BULLET_SPEED
from sprites import Player, Enemy, Bullet, Animation


def load_image(root, path, size):
    return resize(pygame.image.load(root + path), size)


def resize(obj, size):
    return pygame.transform.scale(obj, size)


def load_images():
    return {
        "bg": load_image(RESOURCES, "space_bg.png", WINDOW_SIZE),
        "player": load_image(SHIP_RESOURCES, "1B.png", SHIP_SIZE),
        "enemy": load_image(SHIP_RESOURCES, "8B.png", SHIP_SIZE),
        "bullet": load_image(BEAM_RESOURCES, "B0.png", BULLET_SIZE),
        "boom1": [
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
        "boom2": [
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
    boom = pygame.mixer.Sound(SOUND_RESOURCES + "explosion.wav")
    player.set_volume(1)
    enemy.set_volume(0.1)
    boom.set_volume(0.5)
    return {
        "player": player,
        "enemy": enemy,
        "boom": boom
    }


class Game(object):

    def __init__(self):
        self.images = load_images()
        self.sounds = load_sounds()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsansms", 24)
        self.score = 0
        self.background = self.images["bg"]
        self.text = ""
        self.update_score()
        self.screen = pygame.display.get_surface()
        self.running = True
        self.player_alive = True
        self.player = pygame.sprite.GroupSingle(Player(self.images["player"]))
        self.enemy_speed = 1
        self.enemies = self.create_enemies()
        self.max_enemy_speed = 3
        self.playerBullets = pygame.sprite.Group()
        self.max_enemy_bullets = 6
        self.enemyBullets = pygame.sprite.Group()
        self.animations = pygame.sprite.Group()
        self.game_over = self.font.render("Game Over", True, FONT_COLOR)
        self.end_instructions = self.font.render("Press R to restart or Q to quit", True, FONT_COLOR)
        self.fps = FPS

    def update_score(self):
        self.text = self.font.render(str(self.score), True, FONT_COLOR)

    def create_enemies(self):
        enemy_image = self.images["enemy"]
        enemies = []
        padding = 20
        space_left = (WINDOW_SIZE[0] - 10 * (SHIP_SIZE[0] + padding) + padding) / 2
        for i in range(1, 6):
            inverted = False if i % 2 != 0 else True
            offset_y = i * SHIP_SIZE[1]
            for j in range(0, 10):
                offset_x = space_left + j * padding
                enemies.append(
                    Enemy(enemy_image, (j * SHIP_SIZE[0] + offset_x, i * SHIP_SIZE[1] + offset_y), inverted, self.enemy_speed))
        return pygame.sprite.Group(enemies)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.player_alive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.playerBullets.add(
                        Bullet(self.images["bullet"],
                               (self.player.sprite.rect.centerx - BULLET_SIZE[0] / 2,
                                self.player.sprite.rect.top - 20),
                               PLAYER_BULLET_SPEED
                               ))
                    self.sounds["player"].play()
            elif event.type == pygame.USEREVENT:
                self.spawn_enemy_bullet(
                    random.randint(0,
                                   self.max_enemy_bullets if self.max_enemy_bullets < len(self.enemies) else len(self.enemies)))

    def enemy_hit(self, enemies):
        for enemy in enemies:
            self.score += 1
            self.animations.add(Animation(self.images["boom1"],
                                          (enemy.rect.left, enemy.rect.top),
                                          0.5))
            self.animations.add(Animation(self.images["boom2"],
                                          (enemy.rect.left, enemy.rect.top),
                                          1))
            self.sounds["boom"].play()
        self.update_score()
        if len(self.enemies.sprites()) == 0:
            if self.max_enemy_bullets + 2 <= 50:
                self.max_enemy_bullets += 2
            if self.score % 100 == 0 and self.enemy_speed < self.max_enemy_speed:
                self.enemy_speed += 1

    def player_hit(self, player):
        self.player_alive = False
        pygame.time.set_timer(pygame.USEREVENT, 0)
        self.animations.add(Animation(self.images["boom1"],
                                      (player[0].rect.left, player[0].rect.top),
                                      0.5))
        self.animations.add(Animation(self.images["boom2"],
                                      (player[0].rect.left, player[0].rect.top),
                                      1))
        self.sounds["boom"].play()
        self.fps /= 2

    def spawn_enemy_bullet(self, bullet_number):
        for i in range(bullet_number):
            enemy = self.enemies.sprites()[random.randint(0, len(self.enemies) - 1)]
            self.enemyBullets.add(
                Bullet(self.images["bullet"],
                       (enemy.rect.centerx - BULLET_SIZE[0] / 2,
                        enemy.rect.bottom + 10),
                       ENEMY_BULLET_SPEED)
            )
            self.sounds["enemy"].play()

    def update(self):
        self.player.update()
        self.enemies.update()
        self.playerBullets.update(self.enemies, self.enemy_hit)
        self.enemyBullets.update(self.player, self.player_hit)
        self.animations.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.text,
                         (WINDOW_SIZE[0] / 2 - self.text.get_width() / 2, 10))
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.playerBullets.draw(self.screen)
        self.enemyBullets.draw(self.screen)
        self.animations.draw(self.screen)

    def main_loop(self):
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        res = -1
        respawn = 3000
        while self.running:
            self.events()
            self.draw()
            self.update()
            if len(self.enemies.sprites()) == 0:
                if respawn < 0:
                    self.enemies = self.create_enemies()
                    respawn = 3000
                else:
                    text = self.font.render(str(int(math.ceil(respawn / 1000))) + " seconds to respawn...", True, FONT_COLOR)
                    self.screen.blit(text, (WINDOW_SIZE[0] / 2 - text.get_width() / 2,
                                            WINDOW_SIZE[1] / 2 - text.get_height() / 2))
                    respawn -= self.clock.get_time()
            if not self.player_alive:
                self.game_ended()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.running = False
                    res = 1
                elif keys[pygame.K_q]:
                    self.running = False
            pygame.display.update()
            self.clock.tick(self.fps)
        return res

    def game_ended(self):
        self.screen.blit(self.game_over,
                         (WINDOW_SIZE[0] / 2 - self.game_over.get_width() / 2,
                          WINDOW_SIZE[1] / 2 - self.game_over.get_height() / 2))
        self.screen.blit(self.end_instructions,
                         (WINDOW_SIZE[0] / 2 - self.end_instructions.get_width() / 2,
                          WINDOW_SIZE[1] / 2 + self.game_over.get_height() / 2))


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode(WINDOW_SIZE)
    pygame.mixer.music.load(SOUND_RESOURCES + "xeon6.ogg")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    result = 1
    while result == 1:
        game = Game()
        result = game.main_loop()
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
