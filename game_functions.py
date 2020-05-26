import sys
import pygame
from bullet import Bullet


def check_keydown_events(events, ai_settings, ship, screen, bullets):
    """响应按键"""
    if events.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif events.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif events.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif events.key == pygame.K_q:
        sys.exit()


def check_keyup_events(events, ship):
    """"响应松开"""
    if events.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif events.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ship, ai_settings, screen, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, ship, screen, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, bullets):
    # 每次循环时都会重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitem()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    """更新子弹的位置,并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已经在屏幕外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制则就发射"""
    # 创建一颗子弹,并将其加入到编组bullets 中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
