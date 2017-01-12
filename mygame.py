import pygame
from pygame.locals import *
import random
from sys import exit

SCREEN_WIDTH = 480  # 设置屏幕的宽度
SCREEN_HEIGHT = 800  # 设置屏幕的高度


class Screen(object):
    def __init__(self, height=800, width=480, title='飞机大战', *, backgroundimage, gameoverimage, planeimage):
        pygame.init()
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.background = pygame.image.load(backgroundimage).convert()
        self.game_over = pygame.image.load(gameoverimage)
        self.plane_img = pygame.image.load(planeimage)
        self.player_rect = []
        self.player_rect.append(pygame.Rect(0, 99, 102, 126))  # 玩家飞机图片
        self.player_rect.append(pygame.Rect(165, 360, 102, 126))
        self.player_rect.append(pygame.Rect(165, 234, 102, 126))  # 玩家爆炸图片
        self.player_rect.append(pygame.Rect(330, 624, 102, 126))
        self.player_rect.append(pygame.Rect(330, 498, 102, 126))
        self.player_rect.append(pygame.Rect(432, 624, 102, 126))
        self.player_pos = [200, 600]
        self.bullet_rect = pygame.Rect(1004, 987, 9, 21)
        self.bullet_img = self.plane_img.subsurface(self.bullet_rect)
        self.enemy1_rect = pygame.Rect(534, 612, 57, 43)
        self.enemy1_img = self.plane_img.subsurface(self.enemy1_rect)
        self.enemy1_down_imgs = []
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

        self.enemies1 = pygame.sprite.Group()
        self.enemies_down = pygame.sprite.Group()

        self.shoot_frequency = 0
        self.enemy_frequency = 0
        self.player_down_index = 16
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True


class Getinput(object):
    def __init__(self):
        pass

    def getkey_press(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveup(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def movedown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveleft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveright(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


if __name__ == '__main__':
    gscreen = Screen(backgroundimage='resources/image/background.png', gameoverimage='resources/image/gameover.png',
                     planeimage='resources/image/shoot.png')
    player = Player(gscreen.plane_img, gscreen.player_rect, gscreen.player_pos)

    while gscreen.running:
        gscreen.clock.tick(60)
        if not player.is_hit:
            if gscreen.shoot_frequency % 15 == 0:
                player.shoot(gscreen.bullet_img)
            gscreen.shoot_frequency += 1
            if gscreen.shoot_frequency >= 15:
                gscreen.shoot_frequency = 0
        if gscreen.enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, gscreen.width - gscreen.enemy1_rect.width), 0]
            enemy1 = Enemy(gscreen.enemy1_img, gscreen.enemy1_down_imgs, enemy1_pos)
            gscreen.enemies1.add(enemy1)
        gscreen.enemy_frequency += 1
        if gscreen.enemy_frequency >= 100:
            gscreen.enemy_frequency = 0
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        for enemy in gscreen.enemies1:
            enemy.move()
            if pygame.sprite.collide_circle(enemy, player):
                gscreen.enemies_down.add(enemy)
                gscreen.enemies1.remove(enemy)
                player.is_hit = True
                break
            if enemy.rect.top < 0:
                gscreen.enemies1.remove(enemy)

        enemies1_down = pygame.sprite.groupcollide(gscreen.enemies1, player.bullets, 1, 1)

        for enemy_down in enemies1_down:
            gscreen.enemies_down.add(enemy_down)

        gscreen.screen.fill(0)
        gscreen.screen.blit(gscreen.background, (0, 0))
        if not player.is_hit:
            gscreen.screen.blit(player.image[player.img_index], player.rect)
            player.img_index = int(gscreen.shoot_frequency / 8)
        else:
            player.img_index = int(gscreen.player_down_index / 8)
            gscreen.screen.blit(player.image[player.img_index], player.rect)
            gscreen.player_down_index += 1
            if gscreen.player_down_index > 47:
                gscreen.running = False

        for enemy_down in gscreen.enemies_down:
            if enemy_down.down_index == 0:
                pass
            if enemy_down.down_index > 7:
                gscreen.enemies_down.remove(enemy_down)
                gscreen.score += 1000
                continue

            gscreen.screen.blit(enemy_down.down_imgs[int(enemy_down.down_index / 2)], enemy_down.rect)
            enemy_down.down_index += 1

        player.bullets.draw(gscreen.screen)
        gscreen.enemies1.draw(gscreen.screen)
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(gscreen.score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        gscreen.screen.blit(score_text, text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        key_pressed = pygame.key.get_pressed()

        # 处理键盘事件（移动飞机的位置）
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveup()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.movedown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveleft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveright()
font = pygame.font.Font(None, 48)
text = font.render('Score: ' + str(gscreen.score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = gscreen.screen.get_rect().centerx
text_rect.centery = gscreen.screen.get_rect().centery + 24
gscreen.screen.blit(gscreen.game_over, (0, 0))
gscreen.screen.blit(text, text_rect)

# 显示得分并处理游戏退出
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
