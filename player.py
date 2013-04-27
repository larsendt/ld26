import pygame
from pygame.locals import *
from utils import load_image
from dude import Dude

class Player(Dude):
    def __init__(self, screen_dims):
        Dude.__init__(self, screen_dims)
        self.default_image, self.rect = load_image("res/player_base.png", -1)
        self.left_shoot_image, _ = load_image("res/player_shoot_left.png", -1)
        self.right_shoot_image, _ = load_image("res/player_shoot_right.png", -1)
        self.image = self.default_image

