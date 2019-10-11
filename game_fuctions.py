import sys
from time import sleep
import pygame
from bullet import Bullet
from laser import Laser
from alien import Alien
from explode import Explode
from shields import Shields
from random import *


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        sb.prep_high_score()


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse Cursor
        pygame.mouse.set_visible(False)
        # Rest the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Rest the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()


def check_fleet_edges(ai_settings, aliens):
    # Responds appropriately if any aliens have reached an edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # Drop the entire fleet and change the fleet's direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers):
    """Respond to ship being hit by alien"""
    if stats.ship_left > 0:
        # Decreatse ship_left
        stats.ship_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens, bullets, lasers, explosions
        aliens.empty()
        bullets.empty()
        lasers.empty()
        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the shit got hit
            ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                     bullets=bullets, lasers=lasers)
            break


def check_collision_alien_wall(aliens, shields):
    pygame.sprite.groupcollide(aliens, shields, False, True)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, explosions, shields):
    # Check if the fleet is at an edge
    # Then updates the position of all aliens in the fleet
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        destruction = Explode(ai_settings=ai_settings, screen=screen, ship=ship)
        explosions.add(destruction)
        ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                 bullets=bullets, lasers=lasers)
    check_collision_alien_wall(aliens, shields)
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                        bullets=bullets, lasers=lasers)


def check_bullet_player_collisions(ai_settings, screen, stats, sb, ship, aliens,  bullets, ai_bullets, explosions):
    """Respond to bullet-player collision."""
    # Check for any bullets that hits the player
    # if so, get rid of bullets and player
    collisions = pygame.sprite.groupcollide(ai_bullets, ship, True, True)
    if collisions:
        destruction = Explode(ai_settings=ai_settings, screen=screen, ship=ship)
        explosions.add(destruction)
        ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                 bullets=bullets, lasers=ai_bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, bullets, explosions):
    """Respond to bullet-alien collision."""
    # Check for any bullets that hae hit aliens
    # if so, get rid of the bullets and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                destruction = Explode(ai_settings=ai_settings, screen=screen, ship=alien)
                explosions.add(destruction)
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens)


def check_projectile_shields_collision(projectile, shields):
    pygame.sprite.groupcollide(projectile, shields, True, True)


def check_laser_player_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers):
    """Respond to laser-player collision."""
    # Check for any lasers that have hit player
    # if so, get rid of the alien and player
    collisions = pygame.sprite.spritecollideany(sprite=ship, group=lasers)
    if collisions:
        ship_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens, bullets=bullets,
                 lasers=lasers)


def update_explosions(explosions):
    explosions.update()
    for explosion in explosions.copy():
        if explosion.explode_index >= 5:
            explosions.remove(explosion)


def update_laser(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, shields):
    # Update position of laser and gets reid of old lasers
    lasers.update()

    # Get rid of lasers that have diasspeared
    for laser in lasers.copy():
        if laser.rect.bottom >= ai_settings.screen_height:
            lasers.remove(laser)
    check_projectile_shields_collision(projectile=lasers, shields=shields)
    check_laser_player_collisions(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                                  bullets=bullets, lasers=lasers)


def update_bullets(ai_settings, screen, stats, sb, aliens, bullets, explosions, shields):
    # Update position of bullets and get rid of old bullets
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_projectile_shields_collision(projectile=bullets, shields=shields)

    check_bullet_alien_collisions(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, aliens=aliens,
                                  bullets=bullets, explosions=explosions)


def fire_laser(ai_settings, screen, aliens, lasers):
    for alien in aliens:
        if randrange(100) < alien.shoot_percentage:
            if len(lasers) < ai_settings.ai_max_lasers:
                new_laser = Laser(ai_settings, screen, alien)
                lasers.add(new_laser)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Fire a bullet if limit no reached yet
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Respond to the keypress and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, play_button, explosions, shields):
    # update images on the screen and flip to new screen
    # redraw the screen during each pass through the loop
    screen.fill(ai_settings.bgcolor)

    # Redraw all bullets behind he ship and aliens
    for explosion in explosions.sprites():
        explosion.draw_explode()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for shield in shields.sprites():
        shield.draw()
    for laser in lasers.sprites():
        laser.draw_laser()
    ship.blitme()
    aliens.draw(screen)
    # Draw the score information
    sb.show_score()

    # Draw the play button if hte game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently draw screen visible
    pygame.display.flip()


def get_number_aliens_x(ai_settings, alien_width):
    # Determine the number of aliens per row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # Determine the number of rows of aliens that fit on the screen
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Create an alien and place it in the row.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens):
    # Create a full fleet of aliens
    # Create an alien and find the number of aliens ina row
    # Spacing between each alien is equal to one alie width
    # alien = Alien(ai_settings, screen)
    number_aliens_x = 11
    number_rows = 5

    # Create the fleets
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_walls(ai_settings, screen, shields):
    # Create left wall
    for i in range(0, 17):
        for j in range(0, 6):
            shield = Shields(ai_settings=ai_settings, screen=screen)
            shield.rect.x = (shield.rect.width * i) + 100
            shield.rect.y = (screen.get_rect().height - 100) + (shield.rect.height * j)
            shields.add(shield)

    # Create middle right wall
    for i in range(0, 16):
        for j in range(0, 6):
            shield = Shields(ai_settings=ai_settings, screen=screen)
            shield.rect.x = (shield.rect.width * i) + screen.get_rect().centerx + 150
            shield.rect.y = (screen.get_rect().height - 100) + (shield.rect.height * j)
            shields.add(shield)

    # Create middle middle wall
    for i in range(0, 9):
        for j in range(0, 6):
            shield = Shields(ai_settings=ai_settings, screen=screen)
            shield.rect.x = (shield.rect.width * i) + screen.get_rect().centerx
            shield.rect.y = (screen.get_rect().height - 100) + (shield.rect.height * j)
            shields.add(shield)

        for j in range(0, 6):
            shield = Shields(ai_settings=ai_settings, screen=screen)
            shield.rect.x = screen.get_rect().centerx - (shield.rect.width * i)
            shield.rect.y = (screen.get_rect().height - 100) + (shield.rect.height * j)
            shields.add(shield)
