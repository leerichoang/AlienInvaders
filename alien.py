import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # A class to represent a single alien in the fleet

    def __init__(self, ai_settings, screen):
        # initialize the alien and set it starting position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Set alien default values
        self.shoot_percentage = 10
        self.alien_index = 0
        self.alien_nextframe = 80
        self.alien_clock = pygame.time.get_ticks() + self.alien_nextframe
        self.image_index = [pygame.image.load('images/spritesheets/smallalien000.png'),
                            pygame.image.load('images/spritesheets/smallalien001.png')]

        self.image = self.image_index[self.alien_index]
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Load the alien image and set its rect attribute
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        # Draw the alien at it's current location
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        # Return True if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # Move Aliens to right or left
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        # check if the time for alien image change
        if pygame.time.get_ticks() > self.alien_clock:
            self.alien_index = (self.alien_index + 1) % len(self.image_index)
            self.image = self.image_index[self.alien_index]
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.alien_clock = pygame.time.get_ticks() + self.alien_nextframe
