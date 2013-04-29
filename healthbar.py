import pygame
from pygame.locals import *

from spritesheet import SpriteSheet

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_hp, cur_hp, hb_img, img_dim):
        pygame.sprite.Sprite.__init__(self)
        self.max_hp = max_hp
        self.cur_hp = cur_hp
        self.images = []
        self.barcount = 15

        sp = SpriteSheet(hb_img)
        for i in range(self.barcount):
            self.images.append(sp.image_at((0, -img_dim[1] * (self.barcount - i - 1), img_dim[0], img_dim[1]), -1))

        self.image, self.rect = self.images[self.hp_to_bar_value(self.cur_hp)]

    def set_hp(self, hp):
        self.cur_hp = hp
        self.image, _ = self.images[self.hp_to_bar_value(self.cur_hp)]

    def hp_to_bar_value(self, hp):
        return int((hp / float(self.max_hp)) * (self.barcount-1))

