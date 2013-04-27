#!/usr/bin/env python

import os, sys, random
import pygame
from pygame.locals import *
from healthbar import HealthBar
from badguy import BadGuy
from player import Player
from bullet import Bullet
from ground import Ground
from dude import Dude

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class LD26Main:
    def __init__(self, width=640,height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def load_sprites(self):
        self.player = Player((self.width, self.height))
        self.player_group = pygame.sprite.RenderPlain((self.player))
        self.player_bullet_group = pygame.sprite.RenderPlain()

        self.enemy_group = pygame.sprite.RenderPlain()
        self.enemy_bullet_group = pygame.sprite.RenderPlain()
        self.health_bar_sprites = pygame.sprite.RenderPlain()
        self.max_badguys = 2

        self.ground = Ground((self.width, self.height))

    def go(self):
        self.load_sprites()
        self.clock = pygame.time.Clock()
        while 1:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            while len(self.enemy_group) < self.max_badguys:
                xpos = random.randint(0, self.width-64)
                ypos = random.randint(0, self.height-64)
                h = HealthBar(10, 10)
                b = BadGuy((self.width, self.height), 10, h, (xpos, ypos))
                self.health_bar_sprites.add(h)
                self.enemy_group.add(b)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.player.move(pygame.K_d)
            elif keys[pygame.K_a]:
                self.player.move(pygame.K_a)

            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.player.move(pygame.K_SPACE)

            if keys[pygame.K_RIGHT]:
                if self.player.can_shoot():
                    bullet = Bullet("right", (self.width, self.height), self.player.rect)
                    self.player_bullet_group.add(bullet)
                self.player.shoot(pygame.K_RIGHT)
            elif keys[pygame.K_LEFT]:
                if self.player.can_shoot():
                    bullet = Bullet("left", (self.width, self.height), self.player.rect)
                    self.player_bullet_group.add(bullet)
                self.player.shoot(pygame.K_LEFT)

            for guy in self.enemy_group:
                if guy.is_shooting():
                    bullet = Bullet(guy.shoot_dir, (self.width, self.height), guy.rect)
                    self.enemy_bullet_group.add(bullet)

            # remove bullets that hit terrain
            pygame.sprite.groupcollide(self.enemy_bullet_group, self.ground, True, False)
            pygame.sprite.groupcollide(self.player_bullet_group, self.ground, True, False)

            damaged_guys = pygame.sprite.groupcollide(self.enemy_group, self.player_bullet_group, False, True)
            for d in damaged_guys:
                d.damage(1)
                if d.hp == 0:
                    d.kill()

            guys = self.enemy_group.sprites() + self.player_group.sprites()

            for guy in guys:
                guy.collide_with(self.ground.collisions_for(guy))

            self.player_bullet_group.update()
            self.player_bullet_group.draw(self.screen)
            self.enemy_bullet_group.update()
            self.enemy_bullet_group.draw(self.screen)
            self.enemy_group.update(self.player.rect)
            self.enemy_group.draw(self.screen)
            self.player_group.update()
            self.player_group.draw(self.screen)
            self.health_bar_sprites.update()
            self.health_bar_sprites.draw(self.screen)
            self.ground.update()
            self.ground.draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    win = LD26Main()
    win.go()

