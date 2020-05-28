import pygame


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('arial', 24)
        # 准备初始得分图像
        self.prep_score()
        # 最高得分的图像
        self.prep_high_score()
        self.prep_level()

        # 记录各个兄弟吃屎数
        self.eat_shit()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        # score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.eat_shit1, self.eat_shit1_rect)
        self.screen.blit(self.eat_shit2, self.eat_shit2_rect)
        self.screen.blit(self.eat_shit3, self.eat_shit3_rect)

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()

        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将登记转化为渲染的图像"""
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()

        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def eat_shit(self):
        """将吃屎数目转化"""
        """博吃屎数"""
        # self.score_image = self.font.render(score_str, True, self.text_color,
        #                                     self.ai_settings.bg_color)
        self.eat_shit1 = self.font.render('bo:' + str(self.stats.eat_shit1), True,
                                          self.text_color, self.ai_settings.bg_color)
        """迪吃屎数"""
        self.eat_shit2 = self.font.render('di: ' + str(self.stats.eat_shit2), True,
                                          self.text_color, self.ai_settings.bg_color)
        """鹏吃屎数"""
        self.eat_shit3 = self.font.render('peng: ' + str(self.stats.eat_shit3), True,
                                          self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分下方
        self.eat_shit1_rect = self.eat_shit1.get_rect()
        # 将等级放在得分下方
        self.eat_shit2_rect = self.eat_shit2.get_rect()
        # 将等级放在得分下方
        self.eat_shit3_rect = self.eat_shit3.get_rect()

        self.eat_shit1_rect.left = self.score_rect.left - 900
        self.eat_shit1_rect.top = 20

        self.eat_shit2_rect.left = self.score_rect.left - 800
        self.eat_shit2_rect.top = 20

        self.eat_shit3_rect.left = self.score_rect.left - 700
        self.eat_shit3_rect.top = 20
