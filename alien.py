import random

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像, 并设置其rect 属性
        # self.image = pygame.image.load('images/bo.png')
        pics = ('n_bo.jpg', 'n_di.jpg', 'n_peng.jpg')
        length = len(pics)
        r = random.randint(0, length - 1)
        # 随机选择一张图片
        self.image = pygame.image.load('images/' + pics[r])
        self.name = pics[r]

        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitem(self):
        """"在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人处于屏幕边缘,就返回true"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """"向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor
                   * self.ai_settings.fleet_direction)
        self.rect.x = self.x
