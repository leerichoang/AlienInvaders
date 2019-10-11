import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        # Initialize the ship and set its starting position.
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # set Ship clocks
        self.ship_index = 0
        self.ship_nextframe = 60
        self.ship_clock = pygame.time.get_ticks() + self.ship_nextframe
        self.image_index = [pygame.image.load('images/ship/frontship000.png'),
                            pygame.image.load('images/ship/frontship001.png')]
        self.imageleft_index = [pygame.image.load('images/ship/leftship000.png'),
                                pygame.image.load('images/ship/leftship001.png')]
        self.imageright_index = [pygame.image.load('images/ship/rightship000.png'),
                                 pygame.image.load('images/ship/rightship001.png')]
        # Load the ship image and get its rect.
        # self.image = pygame.image.load('images/ship.bmp')
        self.image = self.image_index[self.ship_index]
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Update the ship's position based on the movement flag.
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update react object from self.center
        self.rect.centerx = self.center
        if pygame.time.get_ticks() > self.ship_clock and self.moving_right:
            self.ship_index = (self.ship_index + 1) % len(self.image_index)
            self.image = self.imageright_index[self.ship_index]
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.ship_clock = pygame.time.get_ticks() + self.ship_nextframe
        elif pygame.time.get_ticks() > self.ship_clock and self.moving_left:
            self.ship_index = (self.ship_index + 1) % len(self.image_index)
            self.image = self.imageleft_index[self.ship_index]
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.ship_clock = pygame.time.get_ticks() + self.ship_nextframe
        elif pygame.time.get_ticks() > self.ship_clock:
            self.ship_index = (self.ship_index + 1) % len(self.image_index)
            self.image = self.image_index[self.ship_index]
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.ship_clock = pygame.time.get_ticks() + self.ship_nextframe

    def blitme(self):
        # Draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center te ship on the screen."""
        self.center = self.screen_rect.centerx
