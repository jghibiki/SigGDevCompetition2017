import math

from pygame.sprite import DirtySprite
import pygame

import config


def init_block_images():
    from items import (
        Grass,
        CopperOreDeposit,
        IronOreDeposit,
        CoalDeposit,
        StoneDeposit,
        Tree,
        Coal,
        Dirt,
        Furnace,
        ScienceStation,
        Printer,
        IndoctrinationChamber,
        WoodenWall,
        IronWall,
        CopperWall,
        StoneWall
    )
    Grass.load_images()
    CopperOreDeposit.load_images()
    IronOreDeposit.load_images()
    CoalDeposit.load_images()
    StoneDeposit.load_images()
    Tree.load_images()
    Coal.load_images()
    Dirt.load_images()

    Furnace.load_images()
    ScienceStation.load_images()
    Printer.load_images()
    IndoctrinationChamber.load_images()

    WoodenWall.load_images()
    IronWall.load_images()
    CopperWall.load_images()
    StoneWall.load_images()

class Block(DirtySprite):

    def __init__(self, x, y, image):
        DirtySprite.__init__(self)

        self.x = x
        self.y = y

        self.image = image
        self.rect = self.image.get_rect().move(
                x * config.image_size[0],
                y * config.image_size[1])


    def update(self, x=0, y=0):
        self.rect.x += x
        self.rect.y += y


    def draw(self, surf, force=False):

        if self.dirty == 1 or self.dirty == 2 or force:
            if self.dirty == 1:
                self.dirty = 0

            return surf.blit(self.image, (self.rect.x, self.rect.y))


