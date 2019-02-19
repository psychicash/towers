from main import pygame
from library1 import get_image

class Cl_Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        pygame.sprite.Sprite.__init__(self)
        self.location = []
        self.location.append(x)
        self.location.append(y)
        img = []
        img.append(get_image(self.set_terrain_image(value)))
        self.image = img[0]
        self.rect = self.image.get_rect()
        self.rect.x = (self.location[1] * 100) + 100
        self.rect.y = (self.location[0] * 100) + 50


    def set_terrain_image(self, value):
        if value == 0:
            return './images/sprites/terrain/tile000.png'
        elif value == 1:
            return './images/sprites/terrain/tile001.png'
        elif value == 2:
            return './images/sprites/terrain/tile002.png'
        elif value == 3:
            return './images/sprites/terrain/tile003.png'
        elif value == 4:
            return './images/sprites/terrain/tile004.png'
        elif value == 5:
            return './images/sprites/terrain/tile005.png'
        elif value == 6:
            return './images/sprites/terrain/tile006.png'
        elif value == 7:
            return './images/sprites/terrain/tile007.png'
        elif value == 8:
            return './images/sprites/terrain/tile008.png'
        elif value == 9:
            return './images/sprites/terrain/tile009.png'
        elif value == 10:
            return './images/sprites/terrain/tile010.png'
        elif value == 11:
            return './images/sprites/terrain/tile011.png'
        elif value == 12:
            return './images/sprites/terrain/tile012.png'
        elif value == 13:
            return './images/sprites/terrain/tile013.png'
        elif value == 14:
            return './images/sprites/terrain/tile014.png'
        elif value == 15:
            return './images/sprites/terrain/tile015.png'

