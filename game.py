import pygame  # 导入pygame
from sys import exit  # 导入sys的exit函数
from pygame.locals import *  # 导入pygame.locals模块
import random  # 导入random模块

SCREEN_WIDTH = 480  # 设置屏幕的宽度
SCREEN_HEIGHT = 800  # 设置屏幕的高度


# 子弹类
class Bullet(pygame.sprite.Sprite):  # 继承Sprite类
    def __init__(self, bullet_img, init_pos):  # 图片，位置的初始化
        pygame.sprite.Sprite.__init__(self)  # 初始化精灵类
        self.image = bullet_img  # 设置图片
        self.rect = self.image.get_rect()  # 设置图片的区域
        self.rect.midbottom = init_pos  # 设置图片位置
        self.speed = 10  # 设置速度

    def move(self):
        self.rect.top -= self.speed  # 子弹移动方法


# 玩家飞机类
class Player(pygame.sprite.Sprite):  # 继承精灵类
    def __init__(self, plane_img, player_rect, init_pos):  # 图片，区域，初始位置
        pygame.sprite.Sprite.__init__(self)  # 初始化精灵类
        self.image = []  # 设置图片列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())  # 将飞机图片的部分分隔，使用保留alpha通道，即透明和不透明
        self.rect = player_rect[0]  # 将飞机的区域获取
        self.rect.topleft = init_pos  # 将区域的位置设置初始化
        self.speed = 8  # 设置速度
        self.bullets = pygame.sprite.Group()  # 生成精灵组实例
        self.img_index = 0  # 图片的序列
        self.is_hit = False  # 判断飞机是否被打中

    def shoot(self, bullet_img):  # 玩家的射击方法
        bullet = Bullet(bullet_img, self.rect.midtop)  # 生成子弹的实例
        self.bullets.add(bullet)  # 添加子弹实例到玩家的子弹组

    def moveUp(self):  # 向上移动的方法
        if self.rect.top <= 0:  # 当遇到顶部时
            self.rect.top = 0  # 设置上顶部为0
        else:
            self.rect.top -= self.speed  # 否则，不断向上

    def moveDown(self):  # 向下移动的方法
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:  # 当遇到底部时
            self.rect.top = SCREEN_HEIGHT - self.rect.height  # 设置一直为常值
        else:
            self.rect.top += self.speed  # 否则，不断向下

    def moveLeft(self):  # 向左的方法
        if self.rect.left <= 0:  # 当遇到左边时
            self.rect.left = 0  # 一直停靠在左边
        else:
            self.rect.left -= self.speed  # 否则，不断向左

    def moveRight(self):  # 向右的方法
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:  # 当遇到右边时
            self.rect.left = SCREEN_WIDTH - self.rect.width  # 停靠右边
        else:
            self.rect.left += self.speed  # 不断向右


class Enemy(pygame.sprite.Sprite):  # 敌人类
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):  # 设置敌人类的初始化
        pygame.sprite.Sprite.__init__(self)  # 初始化精灵类
        self.image = enemy_img  # 设置图片
        self.rect = self.image.get_rect()  # 设置图片的框
        self.rect.topleft = init_pos  # 将左上角设置为初始位置
        self.down_imgs = enemy_down_imgs  # 设置敌机被击毁的图片
        self.speed = 2  # 设置速度
        self.down_index = 0  # 设置击毁序列

    def move(self):  # 设置移动的方法
        self.rect.top += self.speed  # 只能一直向下


pygame.init()  # 初始化所有pygame库的模块
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 设置屏幕
pygame.display.set_caption('feijidazhan')  # 设置屏幕标题
background = pygame.image.load('resources/image/background.png').convert()  # 设置背景
game_over = pygame.image.load('resources/image/gameover.png')  # 设置游戏结束的图片
plane_img = pygame.image.load('resources/image/shoot.png')  # 加载飞机资源图片

player_rect = []  # 初始化飞机区域
player_rect.append(pygame.Rect(0, 99, 102, 126))  # 飞机一
player_rect.append(pygame.Rect(165, 360, 102, 126))  # 飞机二

player_rect.append(pygame.Rect(165, 234, 102, 126))  # 玩家爆炸图片
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]  # 初始化位置
player = Player(plane_img, player_rect, player_pos)  # 生成玩家类

bullet_rect = pygame.Rect(1004, 987, 9, 21)  # 设置子弹框
bullet_img = plane_img.subsurface(bullet_rect)  # 加载子弹图片
enemy1_rect = pygame.Rect(534, 612, 57, 43)  # 设置敌人框
enemy1_img = plane_img.subsurface(enemy1_rect)  # 设置敌人图片

enemy1_down_imgs = []  # 设置敌人被击图片
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))  # 添加图片
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
enemies1 = pygame.sprite.Group()  # 设置敌机精灵组

enemies_down = pygame.sprite.Group()  # 设置敌机被击精灵组
shoot_frequency = 0  # 设置射击频率
enemy_frequency = 0  # 设置敌机频率
player_down_index = 16  # 设置敌机被击的图片顺序
score = 0  # 设置分数
clock = pygame.time.Clock()  # 游戏循环频率
running = True  # 初始化运行状态

while running:  # 开始游戏循环
    clock.tick(60)  # 设置游戏帧率为60
    if not player.is_hit:  # 判断玩家的飞机是否被击
        if shoot_frequency % 15 == 0:  # 设置连续射击
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    if enemy_frequency % 50 == 0:  # 控制生成敌机的频率
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]  # 设置敌机的出现的位置
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)  # 生成敌机实例
        enemies1.add(enemy1)  # 把敌机加入敌机组
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    for bullet in player.bullets:  # 控制子弹的显示运行
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    for enemy in enemies1:  # 控制敌机的运行
        enemy.move()
        if pygame.sprite.collide_circle(enemy, player):  # 判断敌机是否与玩家飞机碰撞
            enemies_down.add(enemy)  # 加入到被击敌机组
            enemies1.remove(enemy)  # 撤出敌机组
            player.is_hit = True  # 设置玩家的飞机被毁
            break

        if enemy.rect.top < 0:  # 判断敌机是否在界面
            enemies1.remove(enemy)

    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)  # 设置敌机与玩家的飞机子弹相碰时，返回被击的敌机实例
    for enemy_down in enemies1_down:  # 把被击的敌机放入击毁组
        enemies_down.add(enemy_down)
    screen.fill(0)  # 绘制屏幕
    screen.blit(background, (0, 0))  # 加入背景图片
    if not player.is_hit:  # 判断玩家飞机是否被击中
        screen.blit(player.image[int(player.img_index)], player.rect)  # 添加飞机图片到屏幕
        player.img_index = shoot_frequency / 8  # 更换图片使飞机有动感
    else:
        player.img_index = player_down_index / 8  #
        screen.blit(player.image[int(player.img_index)], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False
    for enemy_down in enemies_down:  # 敌机被子弹击中的效果显示
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000  # 分数的实现
            continue
        screen.blit(enemy_down.down_imgs[int(enemy_down.down_index / 2)], enemy_down.rect)  # 显示图片
        enemy_down.down_index += 1
    player.bullets.draw(screen)  # 显示子弹
    enemies1.draw(screen)  # 显示敌机
    score_font = pygame.font.Font(None, 36)  # 设置分数字体
    score_text = score_font.render(str(score), True, (128, 128, 128))  # 分数的显示效果
    text_rect = score_text.get_rect()  # 设置文字框
    text_rect.topleft = [10, 10]  # 放置文字的位置
    screen.blit(score_text, text_rect)  # 显示出分数

    pygame.display.update()  # 刷新屏幕
    for event in pygame.event.get():  # 处理游戏退出
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_pressed = pygame.key.get_pressed()  # 获取键盘的输入

    if key_pressed[K_w] or key_pressed[K_UP]:  # 处理键盘输入的处理事件
        player.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()

font = pygame.font.Font(None, 48)  # 设置字体
text = font.render('Score: ' + str(score), True, (255, 0, 0))  # 设置字体样式
text_rect = text.get_rect()  # 设置字体框
text_rect.centerx = screen.get_rect().centerx  # 设置X坐标
text_rect.centery = screen.get_rect().centery + 24  # 设置Y坐标
screen.blit(game_over, (0, 0))  # 显示游戏结束画面
screen.blit(text, text_rect)  # 显示分数

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
