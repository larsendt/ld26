import pygame
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = name
    try:
        image = pygame.image.load(fullname).convert()
        image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def mtd_vector(rect1, rect2):
    amin = rect1.left, rect1.top
    amax = rect1.right, rect1.bottom
    bmin = rect2.left, rect2.top
    bmax = rect2.right, rect2.bottom

    left = bmin[0] - amax[0]
    right = bmax[0] - amin[0]
    top = bmin[1] - amax[1]
    bottom = bmax[1] - amin[1]

    mtd = [0, 0]

    if left > 0 or right < 0 or top > 0 or bottom < 0:
        print "nocollide"
        return

    if abs(left) < right:
        mtd[0] = left
    else:
        mtd[0] = right

    if abs(top) < bottom:
        mtd[1] = top
    else:
        mtd[1] = bottom

    if abs(mtd[0]) > abs(mtd[1]):
        mtd[0] = 0
    else:
        mtd[1] = 0

    return mtd
