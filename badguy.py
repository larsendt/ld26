import pygame
import random
from pygame.locals import *
from utils import load_image
from dude import Dude
from enemyai import EnemyAI

class BadGuy(Dude):
    def __init__(self, screen_dims, hp, health_bar, pos):
        Dude.__init__(self, screen_dims)
        self.default_image, self.rect = load_image("res/grunt_base.png", -1)
        self.left_shoot_image, _ = load_image("res/grunt_shoot_left.png", -1)
        self.right_shoot_image, _ = load_image("res/grunt_shoot_right.png", -1)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image = self.default_image
        self.health_bar = health_bar
        self.health_bar.rect.x = self.rect.x
        self.health_bar.rect.bottom = self.rect.y
        self.hp = hp
        self.ai = EnemyAI(self.rect)
        self.shot_interval = 80 + random.randint(0, 20)
        self.jump_power = -5 - random.randint(0, 5)

    def damage(self, amt):
        if self.hp > 0:
            self.hp = max(self.hp - amt, 0)
            self.health_bar.set_hp(self.hp)

    def kill(self):
        self.health_bar.kill()
        pygame.sprite.Sprite.kill(self)

    def update(self, player_rect):
        Dude.update(self)
        self.health_bar.rect.x = self.rect.x
        self.health_bar.rect.bottom = self.rect.y

        self.ai.update(player_rect, self.rect, not self.grounded)
        direction = self.ai.shoot_dir()
        if direction == "left":
            self.shoot(K_RIGHT)
        elif direction == "right":
            self.shoot(K_LEFT)

        movedir, jmp = self.ai.move_dir()
        if movedir == "left":
            self.move(K_a)
        elif movedir == "right":
            self.move(K_d)

        if jmp:
            self.jump()
