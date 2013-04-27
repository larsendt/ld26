import pygame
from pygame.locals import *
from utils import load_image

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, screen_dims, player_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("res/bullet.png")
        self.rect.y = player_rect.y + 12
        self.screen_dims = screen_dims
        if direction == "left":
            self.velocity = -10
            self.rect.x = player_rect.x
        else:
            self.velocity = 10
            self.rect.x = player_rect.right

    def update(self):
        self.rect.x += self.velocity
        if self.rect.x > (self.screen_dims[0] + 20) or self.rect.x < -20:
            self.kill()

