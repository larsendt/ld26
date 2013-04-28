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
        pxarray = pygame.PixelArray(pygame.image.load("res/levels/level1.png"))
        sz = 64

        for colnum, col in enumerate(pxarray):
            for rownum, pixel in enumerate(col):
                if pixel == 0:
                    lt = LevelTile((colnum * sz, rownum * sz))
                    self.add(lt)

    def collisions_for(self, sprite):
        return map(lambda x: x.rect, pygame.sprite.spritecollide(sprite, self, False))


