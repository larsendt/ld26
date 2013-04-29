#!/usr/bin/env python

import os, sys, random
import pygame
from pygame.locals import *
from healthbar import HealthBar
from badguy import BadGuy
from player import Player
from bullet import Bullet
from level import Level
from dude import Dude
from cameraspritegroup import CameraSpriteGroup
from backdrop import Backdrop
from menu import Menu
from win import Win
from die import Die

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class LD26Main:
    def __init__(self, width=800,height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.state = "menu"

    def load_sprites(self):
        self.player_group = CameraSpriteGroup()
        self.player_bullet_group = CameraSpriteGroup()

        self.enemy_group = CameraSpriteGroup()
        self.enemy_bullet_group = CameraSpriteGroup()
        self.health_bar_sprites = CameraSpriteGroup()
        self.max_badguys = 0
        self.guys_killed = 0

        self.levels = [{"img":"res/levels/level1.png", "badguys":2, "goal":10}, {"img":"res/levels/level2.png", "badguys":5, "goal":10}]
        self.cur_level = 0

        self.load_level(0)
        self.menu = Menu()
        self.win = Win()
        self.die = Die()

    def load_level(self, levelnum):
        if levelnum >= len(self.levels):
            self.state = "win"
        else:
            leveldict = self.levels[levelnum]
            self.player = Player((self.width, self.height))
            self.player_group.add(self.player)
            self.level = Level((self.width, self.height), leveldict["img"])
            self.bdrop1 = Backdrop(self.level.dims, 1)
            self.bdrop2 = Backdrop(self.level.dims, 2)
            self.max_badguys = leveldict["badguys"]
            self.guys_killed = 0
            self.kill_goal = leveldict["goal"]

    def go(self):
        self.load_sprites()
        self.clock = pygame.time.Clock()
        while 1:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.state == "game":
                            self.state = "menu"
                        else:
                            sys.exit()

                    elif event.key == K_RETURN:
                        if self.state == "menu":
                            self.state = "game"
                        elif self.state == "win" or self.state == "die":
                            self.load_level(0)
                            self.state = "game"

            if self.state == "menu":
                self.do_menu()
            elif self.state == "game":
                self.do_main_game()
            elif self.state == "win":
                self.do_win()
            else:
                self.do_die()

            pygame.display.flip()

    def do_die(self):
        self.die.update()
        self.die.draw(self.screen)

    def do_win(self):
        self.win.update()
        self.win.draw(self.screen)

    def do_menu(self):
        self.menu.update()
        self.menu.draw(self.screen)

    def do_main_game(self):
        if self.guys_killed > self.kill_goal:
            self.cur_level += 1
            self.load_level(self.cur_level)

        offset = (self.width / 2) - self.player.rect.x, (self.height / 1.5) - self.player.rect.y
        while len(self.enemy_group) < self.max_badguys:
            xpos = random.randint(0, self.width-64) - offset[0]
            ypos = random.randint(0, self.height-64) - offset[1]
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
                bullet = Bullet("right", self.level.size, self.player.rect)
                self.player_bullet_group.add(bullet)
            self.player.shoot(pygame.K_RIGHT)
        elif keys[pygame.K_LEFT]:
            if self.player.can_shoot():
                bullet = Bullet("left", self.level.size, self.player.rect)
                self.player_bullet_group.add(bullet)
            self.player.shoot(pygame.K_LEFT)

        for guy in self.enemy_group:
            if guy.is_shooting():
                bullet = Bullet(guy.shoot_dir, self.level.size, guy.rect)
                self.enemy_bullet_group.add(bullet)

        # remove bullets that hit terrain
        pygame.sprite.groupcollide(self.enemy_bullet_group, self.level, True, False)
        pygame.sprite.groupcollide(self.player_bullet_group, self.level, True, False)

        damaged_guys = pygame.sprite.groupcollide(self.enemy_group, self.player_bullet_group, False, True)
        for d in damaged_guys:
            d.damage(1)
            if d.hp == 0:
                self.guys_killed += 1
                d.kill()

        guys = self.enemy_group.sprites() + self.player_group.sprites()

        for guy in guys:
            if guy.rect.top > self.level.bottom():
                guy.kill()
                if isinstance(guy, Player):
                    self.state = "die"
            else:
                guy.collide_with(self.level.collisions_for(guy))

        self.bdrop2.update()
        self.bdrop2.draw(self.screen, (offset[0]/4, offset[1]/4))
        self.bdrop1.update()
        self.bdrop1.draw(self.screen, (offset[0]/2, offset[1]/2))
        self.player_bullet_group.update()
        self.player_bullet_group.draw(self.screen, offset)
        self.enemy_bullet_group.update()
        self.enemy_bullet_group.draw(self.screen, offset)
        self.enemy_group.update(self.player.rect)
        self.enemy_group.draw(self.screen, offset)
        self.player_group.update()
        self.player_group.draw(self.screen, offset)
        self.health_bar_sprites.update()
        self.health_bar_sprites.draw(self.screen, offset)
        self.level.update()
        self.level.draw(self.screen, offset)

if __name__ == "__main__":
    win = LD26Main()
    win.go()

