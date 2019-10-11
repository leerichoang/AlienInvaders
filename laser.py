import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    """A class to manage bullets firing from the ship"""

    def __init__(self, ai_settings, screen, alien):
        # Create a laser object at the alien's current position
        super(Laser, self).__init__()
        self.settings = ai_settings
        self.screen = screen
        self.alien = alien

        # Set Laser default value
        self.laser_index = 0
        self.laser_frame = 60
        self.laser_clock = pygame.time.get_ticks() + self.laser_frame
        self.image_index = [pygame.image.load('images/bullet/lazer00.png'),
                            pygame.image.load('images/bullet/lazer01.png')]
        self.image = self.image_index[self.laser_index]
        self.image = pygame.transform.scale(self.image, (4, 4))

        # load the laser image and set it's rect attribute
        self.rect = self.image.get_rect()

        # store the bullet's position as a decimal value
        self.rect.x = float(self.alien.rect.x)
        self.rect.y = float(self.alien.rect.y)
        self.y = self.rect.y
        self.speed_factor = self.settings.bullet_speed_factor

    def update(self):
        # Move the bullet down the screen
        self.y += self.speed_factor
        self.rect.y = self.y

        # Check if the time for alien image changes
        if pygame.time.get_ticks() > self.laser_clock:
            self.laser_index = (self.laser_index + 1) % len(self.image_index)
            self.image = self.image_index[self.laser_index]
            self.image = pygame.transform.scale(self.image, (4, 4))
            self.laser_clock = pygame.time.get_ticks() + self.laser_frame

    def draw_laser(self):
        # Draw the laser on the screen
        self.screen.blit(self.image, self.rect)
