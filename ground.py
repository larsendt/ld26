import pygame
from pygame.locals import *
from utils import load_image

class GroundTile(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("res/ground.png")
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Ground(pygame.sprite.RenderPlain):
    def __init__(self, screen_dims):
        pygame.sprite.RenderPlain.__init__(self)
        tilecount = (screen_dims[0] / 64) + 1
        for i in range(tilecount):
            tile = GroundTile((i * 64, screen_dims[1] - 64))
            self.add(tile)

        tile = GroundTile((3*64, screen_dims[1] - 128))
        self.add(tile)
        tile = GroundTile((5*64, screen_dims[1] - 256))
        self.add(tile)

    def collisions_for(self, sprite):
        return map(lambda x: x.rect, pygame.sprite.spritecollide(sprite, self, False))


