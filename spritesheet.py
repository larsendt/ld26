import pygame
from pygame.locals import *

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
            self.sheet = pygame.transform.scale(self.sheet, (self.sheet.get_width() * 2, self.sheet.get_height() * 2))
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    def image_at(self, rectangle, colorkey = None):
        rect = pygame.Rect(rectangle)
        rect.width *= 2
        rect.height *= 2
        rect.y *= 2
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, rect

