from main import pygame
from library1 import get_image

class Cl_Launcher(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.location = []
        self.location.append(x)
        self.location.append(y)
        img = get_image('./images/sprites/launcher_icon.png')
        self.image = img
        self.rect = self.image.get_rect()

        self.rect.x = (self.location[1] * 100) + 100
        self.rect.y = (self.location[0] * 100) + 50