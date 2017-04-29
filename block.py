import math

from pygame.sprite import DirtySprite
import pygame

import config

def init_block_images():
    from items import CopperOreDeposit, IronOreDeposit, CoalDeposit
    Grass.load_images()
    CopperOreDeposit.load_images()
    IronOreDeposit.load_images()
    CoalDeposit.load_images()

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




################
# Block Types
################

# Map Layer Blocks

class Grass(Block):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/grass.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y):
        Block.__init__(self, x, y, Grass.image)

