import pygame
from pygame.locals import *
from utils import load_image

class MenuSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("res/menu.png")


class Menu(pygame.sprite.RenderPlain):
    def __init__(self):
        pygame.sprite.RenderPlain.__init__(self)
        self.add(MenuSprite())
