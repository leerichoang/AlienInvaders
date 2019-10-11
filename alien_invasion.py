import pygame
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from button import Button
from ship import Ship
# from laser import Laser
# from explode import Explode
# from alien import Alien
import game_fuctions as gf


def run_game():
    # Initializes the game and crete a screen obj
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")
    # Create an instances to start game stats and create Scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    lasers = Group()
    explodes = Group()
    shields = Group()
    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens)
    gf.create_walls(ai_settings=ai_settings, screen=screen, shields=shields)
    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.fire_laser(ai_settings, screen, aliens, lasers)
            gf.update_laser(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship,
                            aliens=aliens, bullets=bullets, lasers=lasers, shields=shields)
            gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, aliens=aliens,
                              bullets=bullets, explosions=explodes, shields=shields)
            gf.update_aliens(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                             bullets=bullets, lasers=lasers, explosions=explodes, shields=shields)
            gf.update_explosions(explodes)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, play_button, explodes, shields)


run_game()
