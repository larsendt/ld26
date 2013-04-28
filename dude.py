import pygame
from pygame.locals import *
from utils import load_image, mtd_vector

class Dude(pygame.sprite.Sprite):
    def __init__(self, screen_dims):
        pygame.sprite.Sprite.__init__(self)
        self.default_image, self.rect = load_image("res/dude_base.png", -1)
        self.left_shoot_image, _ = load_image("res/dude_shoot_left.png", -1)
        self.right_shoot_image, _ = load_image("res/dude_shoot_right.png", -1)
        self.image = self.default_image
        self.max_v = 8
        self.velocity = [0, 0]
        self.friction = 0.5
        self.gravity = 0.3
        self.jump_power = -8
        self.shoot_dir = None
        self.shot_interval = 8
        self.shoot_count = 0
        self.grounded = False
        self.screen_dims = screen_dims

    def can_shoot(self):
        return self.shoot_count == 0 or self.shoot_count >= self.shot_interval

    def move(self, key):
        if key == K_a:
            self.velocity[0] = max(self.velocity[0] - 1, -self.max_v)
        elif key == K_d:
            self.velocity[0] = min(self.velocity[0] + 1, self.max_v)
        elif key == K_SPACE:
            self.jump()

    def is_shooting(self):
        return self.shoot_dir != None and self.can_shoot()

    def jump(self):
        if self.grounded:
            self.velocity[1] = self.jump_power
            # BLARHG COLLISION CRAP
            self.rect.bottom -= 1
            self.grounded = False

    def shoot(self, key):
        if not self.shoot_dir:
            self.shoot_count = 0
            if key == K_RIGHT:
                self.shoot_dir = "right"
            elif key == K_LEFT:
                self.shoot_dir = "left"

    def collide_with(self, collisions):
        if not collisions:
            self.grounded = False
            return

        for rect in collisions:
            mtd = mtd_vector(self.rect, rect)
            #self.rect.x += mtd[0]
            #self.rect.y += mtd[1]

            if mtd[1] < 0: # collision from above
                self.velocity[1] = min(0, self.velocity[1])
                self.rect.bottom = rect.top + 1
                self.grounded = True
            elif mtd[1] > 0: # from below
                self.velocity[1] = max(0, self.velocity[1])
                self.rect.top = rect.bottom
            elif mtd[0] < 0: # from the left
                if self.rect.bottom - rect.top > 1:
                    self.velocity[0] = min(0, self.velocity[0])
                    self.rect.right = rect.left + 1
            elif mtd[0] > 0: # from the right
                if self.rect.bottom - rect.top > 1:
                    self.velocity[0] = max(0, self.velocity[0])
                    self.rect.left = rect.right - 1


    def update(self):
        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - self.friction)
        elif self.velocity[0] < 0:
            self.velocity[0] = min(0, self.velocity[0] + self.friction)

        if not self.grounded:
            self.velocity[1] += self.gravity
            self.rect.move_ip(self.velocity[0], self.velocity[1])
        else:
            self.velocity[1] = max(0, self.velocity[1])
            self.rect.move_ip(self.velocity[0], self.velocity[1])

        if self.shoot_dir == "left":
            self.image = self.left_shoot_image
            self.shoot_count += 1
        elif self.shoot_dir == "right":
            self.image = self.right_shoot_image
            self.shoot_count += 1
        else:
            self.image = self.default_image

        if self.shoot_count >= self.shot_interval:
            self.shoot_dir = None


