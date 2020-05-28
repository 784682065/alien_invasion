import pygame
from button import Button
from game_stats import GameStats
from pygame.sprite import Group
from scoreboard import Scoreboard
from settings import Setting
from ship import Ship
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Setting()
    screen = pygame.display.set_mode(
        (
            ai_settings.screen_width,
            ai_settings.screen_height
        )
    )
    # background = pygame.image.load('images/7.jpg').convert()
    # screen.blit(background, (0, 0))  # 对齐的坐标

    pygame.display.set_caption("正道 德 光")
    # 创建play 按钮
    play_button = Button(ai_settings, screen, "Play")

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建外星人群
    aliens = Group()

    # 创建一个外星人
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ship, ai_settings, screen, bullets,
                        play_button, stats, aliens, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                         play_button, sb)


run_game()
