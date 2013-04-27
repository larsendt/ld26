import pygame
from pygame.locals import *
import random

class EnemyAI:
    def __init__(self, rect):
        self.target_rect = pygame.Rect(0, 0, 0, 0)
        self.rect = rect
        self.jumping = False
        self.close_dist = 70
        self.far_dist = 120

    def update(self, target_rect, rect, jumping):
        self.target_rect = target_rect
        self.rect = rect
        self.jumping = jumping

    def shoot_dir(self):
        if self.rect.y >= self.target_rect.y and self.rect.y < self.target_rect.bottom:
            if self.rect.x > self.target_rect.x:
                return "right"
            else:
                return "left"

    def move_dir(self):
        direction = None
        jump = False
        if self.rect.left > self.target_rect.left:
            dist = self.rect.left - self.target_rect.left
            if dist < self.close_dist:
                direction = "right"
                jump = True
            elif dist > self.far_dist:
                direction = "left"
        elif self.rect.right < self.target_rect.right:
            dist = self.target_rect.right - self.rect.right
            if dist < self.close_dist:
                direction = "left"
                jump = True
            elif dist > self.far_dist:
                direction = "right"
        else:
            direction = random.choice(("left", "right"))

        jmpdelay = 30 + random.randint(0, 200)
        if (self.target_rect.y + jmpdelay) < self.rect.y and not self.jumping:
            jump = True

        random_jump = random.uniform(0, 1) > 0.9
        if jump and not random_jump:
            jump = False

        return direction, jump
