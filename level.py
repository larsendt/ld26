import pygame
from pygame.locals import *
from utils import load_image
from cameraspritegroup import CameraSpriteGroup

class LevelTile(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("res/leveltile.png")
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Level(CameraSpriteGroup):
    def __init__(self, screen_dims):
        pygame.sprite.RenderPlain.__init__(self)
        pixarray = pygame.PixelArray(pygame.image.load("res/levels/level1.png"))
        self.tilesize = 64
        self.dims = len(pixarray), len(pixarray[0])

        for colnum, col in enumerate(pixarray):
            for rownum, pixel in enumerate(col):
                if pixel == 0:
                    lt = LevelTile((colnum * self.tilesize, rownum * self.tilesize))
                    self.add(lt)

    def collisions_for(self, sprite):
        return map(lambda x: x.rect, pygame.sprite.spritecollide(sprite, self, False))

    def bottom(self):
        return self.dims[1] * self.tilesize
