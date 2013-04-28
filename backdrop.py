import pygame
from pygame.locals import *
from utils import load_image
import random
from cameraspritegroup import CameraSpriteGroup
from spritesheet import SpriteSheet

tiles = {1:["res/tiles/layer1/building1.png", "res/tiles/layer1/building2.png"],
         2:["res/tiles/layer2/building1.png", "res/tiles/layer2/building2.png", "res/tiles/layer2/building3.png"]}

tops = {1:["res/tiles/layer1/buildingtop1.png"],
        2:["res/tiles/layer2/buildingtop1.png"]}

class BackdropTile(pygame.sprite.Sprite):
    def __init__(self, pos, imgpath):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(imgpath, (0, 0, 0))
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class TopTile(pygame.sprite.Sprite):
    def __init__(self, pos, imgpath):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.rects = []

        sp = SpriteSheet(imgpath)

        for i in range(5):
            img, rct = sp.image_at((0, -i*32, 32, 32), colorkey=(0, 0, 0))
            self.images.append(img)
            self.rects.append(rct)

        self.rect = self.rects[0]
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image = self.images[0]
        self.sprite_counter = 0
        self.counter_max = 20 + random.randint(0, 10)
        self.cur_sprite_idx = 0

    def update(self):
        self.sprite_counter += 1
        if self.sprite_counter > self.counter_max:
            self.sprite_counter = 0
            self.cur_sprite_idx = (self.cur_sprite_idx + 1) % len(self.images)
            self.image = self.images[self.cur_sprite_idx]

class Backdrop(CameraSpriteGroup):
    def __init__(self, level_dims, layer):
        pygame.sprite.RenderPlain.__init__(self)
        self.sz = 64

        for i in range(level_dims[0]):
            top = random.randint(0, level_dims[1])
            tile = TopTile((i*self.sz, top*self.sz), random.choice(tops[layer]))
            self.add(tile)
            for j in range(top+1, level_dims[1]):
                tile = BackdropTile((i*self.sz, j*self.sz), random.choice(tiles[layer]))
                self.add(tile)
