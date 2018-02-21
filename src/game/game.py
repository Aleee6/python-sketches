import random
import sys
import pygame
import math
from settings import WINDOW_SIZE, SHIP_SIZE, BULLET_SIZE, \
    CAPTION, FPS, FONT_COLOR, PLAYER_BULLET_SPEED, ENEMY_BULLET_SPEED
from sprites import Player, Enemy, Bullet, Animation
import resource_handler as res


class Game(object):

    def __init__(self):
        self.images = res.load_images()
        self.sounds = res.load_sounds()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsansms", 24)
        self.score = 0
        self.background = self.images[res.BACKGROUND_IMAGE]
        self.text = ""
        self.update_score()
        self.screen = pygame.display.get_surface()
        self.running = True
        self.player_alive = True
        self.player = pygame.sprite.GroupSingle(Player(self.images[res.PLAYER_SPRITE]))
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
        enemy_image = self.images[res.ENEMY_SPRITE]
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
                        Bullet(self.images[res.BULLET_SPRITE],
                               (self.player.sprite.rect.centerx - BULLET_SIZE[0] / 2,
                                self.player.sprite.rect.top - 20),
                               PLAYER_BULLET_SPEED
                               ))
                    self.sounds[res.PLAYER_SOUND].play()
            elif event.type == pygame.USEREVENT:
                self.spawn_enemy_bullet(
                    random.randint(0,
                                   self.max_enemy_bullets if self.max_enemy_bullets < len(self.enemies) else len(self.enemies)))

    def enemy_hit(self, enemies):
        for enemy in enemies:
            self.score += 1
            self.add_explosion(enemy)
        self.update_score()
        if len(self.enemies.sprites()) == 0:
            if self.max_enemy_bullets + 2 <= 50:
                self.max_enemy_bullets += 2
            if self.score % 100 == 0 and self.enemy_speed < self.max_enemy_speed:
                self.enemy_speed += 1

    def player_hit(self, player):
        self.player_alive = False
        pygame.time.set_timer(pygame.USEREVENT, 0)
        self.add_explosion(player[0])
        self.fps /= 2

    def add_explosion(self, sprite):
        self.animations.add(Animation(self.images[res.EXPLOSION_SPRITES_1],
                                      (sprite.rect.left, sprite.rect.top),
                                      0.5))
        self.animations.add(Animation(self.images[res.EXPLOSION_SPRITES_2],
                                      (sprite.rect.left, sprite.rect.top),
                                      1))
        self.sounds[res.EXPLOSION_SOUND].play()

    def spawn_enemy_bullet(self, bullet_number):
        for i in range(bullet_number):
            enemy = self.enemies.sprites()[random.randint(0, len(self.enemies) - 1)]
            self.enemyBullets.add(
                Bullet(self.images[res.BULLET_SPRITE],
                       (enemy.rect.centerx - BULLET_SIZE[0] / 2,
                        enemy.rect.bottom + 10),
                       ENEMY_BULLET_SPEED)
            )
            self.sounds[res.ENEMY_SOUND].play()

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
        key = -1
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
                    key = 1
                elif keys[pygame.K_q]:
                    self.running = False
            pygame.display.update()
            self.clock.tick(self.fps)
        return key

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
    pygame.mixer.music.load(res.BACKGROUND_MUSIC)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    result = 1
    while result == 1:
        game = Game()
        result = game.main_loop()
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
