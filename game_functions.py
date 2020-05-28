import sys
from time import sleep

import pygame
from alien import Alien
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


def check_play_button(stats, play_button, mouse_x, mouse_y,
                      ai_settings, screen, ship, aliens, bullets,
                      sb):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        # 清空外星人列表he子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群外星人, 并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ship, ai_settings, screen, bullets,
                 play_button, stats, aliens,sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, ship, screen, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y,
                              ai_settings, screen, ship, aliens, bullets,
                              sb)


def update_screen(ai_settings, screen, stats, ship, aliens,
                  bullets, play_button, sb):
    # 每次循环时都会重绘屏幕
    screen.fill(ai_settings.bg_color)
    # background = pygame.image.load('images/7.jpg').convert()
    # screen.blit(background, (0, 0))  # 对齐的坐标

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitem()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets,
                   stats, sb):
    """更新子弹的位置,并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已经在屏幕外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen,
                                  ship, aliens, bullets,
                                  stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,
                                  stats, sb):
    # 检查是否有子弹集中了外星人
    # 如果是这样, 就删除相应的外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens,
                                            True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹并且新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制则就发射"""
    # 创建一颗子弹,并将其加入到编组bullets 中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可以容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_setting, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_setting.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人, 并计算一行可容纳多少外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        # 创建第一行外星人
        for alien_number in range(number_aliens_x):
            # 创建第一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移动,并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """有外星人达到边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕低端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘,并更新外星人的位置"""
    check_fleet_edges(ai_settings, aliens)

    """更新外星人群众所有外星人的位置"""
    aliens.update()

    # 检测外星人he飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # 检测是否外星人到达屏幕低端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到"""
    # 将ship left减去1
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # 清空外星人列表与子弹列表
        aliens.empty()
        bullets.empty()
        ai_settings.increase_speed()

        # 创建一群新的外星人, 并将飞船放到屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
