import pygame
from pygame.sprite import Sprite


class Shields(Sprite):

    def __init__(self, ai_settings, screen):
        super(Shields, self).__init__()

        self.settings = ai_settings
        self.screen = screen
        self.color = (189, 183, 107)
        self.rect = pygame.Rect((0, 0), (10, 10))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
