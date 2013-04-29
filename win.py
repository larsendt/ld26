import pygame
from pygame.locals import *
from utils import load_image

class WinSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("res/win.png")


class Win(pygame.sprite.RenderPlain):
    def __init__(self):
        pygame.sprite.RenderPlain.__init__(self)
        self.add(WinSprite())
