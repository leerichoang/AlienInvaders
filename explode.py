import pygame
from pygame.sprite import Sprite


class Explode(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super(Explode, self).__init__()
        self.screen = screen
        self.ship = ship
        self.ai_settings = ai_settings

        # Set explode default values
        self.explode_index = 0
        self.explode_nextframe = 20
        self.explode_clock = pygame.time.get_ticks() + self.explode_nextframe
        self.image_index = [pygame.image.load('images/explode/boom000.png'),
                            pygame.image.load('images/explode/boom001.png'),
                            pygame.image.load('images/explode/boom002.png'),
                            pygame.image.load('images/explode/boom003.png'),
                            pygame.image.load('images/explode/boom004.png')]
        self.image = self.image_index[self.explode_index]
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Load the explosion image and set it's rect attributes
        self.rect = self.image.get_rect()

        # Start each new explosion at the point of the ship
        self.rect.y = float(self.ship.rect.y)
        self.rect.x = float(self.ship.rect.x)

    def update(self):
        if pygame.time.get_ticks() > self.explode_clock:
            self.explode_index = self.explode_index + 1
            if self.explode_index < len(self.image_index):
                self.image = self.image_index[self.explode_index]
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.explode_clock = pygame.time.get_ticks() + self.explode_nextframe

    def draw_explode(self):
        # Draw Explosion on the screen
        self.screen.blit(self.image, self.rect)
