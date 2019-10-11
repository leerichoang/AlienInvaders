import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # A class to manage bullets firing from the ship

    def __init__(self, ai_settings, screen, ship):
        # Create a bullet object at the ship's current position
        super(Bullet, self).__init__()
        self.screen = screen
        self.ship = ship
        # Set Bullet default values
        self.bullet_index = 0
        self.bullet_frame = 60
        self.bullet_clock = pygame.time.get_ticks() + self.bullet_frame
        self.image_index = [pygame.image.load('images/bullet/playerbullet000.png'),
                            pygame.image.load('images/bullet/playerbullet001.png')]
        self.image = self.image_index[self.bullet_index]
        self.image = pygame.transform.scale(self.image, (20, 20))

        # load the bullet image and set its rect attributes
        self.rect = self.image.get_rect()

        # Store the bullet's position as a decimal value
        self.rect.y = float(self.ship.rect.y)
        self.y = self.rect.y
        self.rect.x = float(self.ship.rect.x + 5)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # Move the bullet up the screen
        self.y -= self.speed_factor
        self.rect.y = self.y

        # Check if the time for alien image change
        if pygame.time.get_ticks() > self.bullet_clock:
            self.bullet_index = (self.bullet_index + 1) % len(self.image_index)
            self.image = self.image_index[self.bullet_index]
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.bullet_clock = pygame.time.get_ticks() + self.bullet_frame

    def draw_bullet(self):
        # Draw the bullet to the screen
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
