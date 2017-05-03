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
        Coal,
        Dirt,
        Furnace,
        ScienceStation,
        Printer,
        IndoctrinationChamber,
        IronWall,
        StoneWall,
        Stone,
        Coal,
        Iron,
        Copper,
        Stockpile,
        ReanimationChamber,
        BuildingMarker,
        DeliveryBot
    )
    Grass.load_images()
    CopperOreDeposit.load_images()
    IronOreDeposit.load_images()
    CoalDeposit.load_images()
    StoneDeposit.load_images()
    Coal.load_images()
    Dirt.load_images()

    Furnace.load_images()
    ScienceStation.load_images()
    Printer.load_images()
    IndoctrinationChamber.load_images()
    ReanimationChamber.load_images()
    DeliveryBot.load_images()

    IronWall.load_images()
    StoneWall.load_images()

    Stone.load_images()
    Coal.load_images()
    Iron.load_images()
    Copper.load_images()

    Stockpile.load_images()
    BuildingMarker.load_images()

class Block(DirtySprite):

    def __init__(self, x, y, image, viewport):
        DirtySprite.__init__(self)

        self.viewport = viewport

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


    def mouse_collide(self, pos=None):
        rect = self.image.get_rect()
        rect = pygame.Rect(
                self.x * config.image_size[0],
                self.y * config.image_size[1],
                config.image_size[0], config.image_size[1])

        if not pos:
            pos = pygame.mouse.get_pos()

        corrected_pos = ( pos[0] + self.viewport.v_rect.x, pos[1] + self.viewport.v_rect.y )
        collided = rect.collidepoint(corrected_pos)

        return collided
