import pygame

import config
from item_types import *

class CopperOreDeposit(Item, OreDeposit):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/copper_ore.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, CopperOreDeposit.image, viewport)
        OreDeposit.__init__(self, quantity)



class IronOreDeposit(Item, OreDeposit):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/iron_ore.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity = 100):
        Item.__init__(self, x, y, IronOreDeposit.image, viewport)
        OreDeposit.__init__(self, quantity)


class CoalDeposit(Item, OreDeposit):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/coal.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, CoalDeposit.image, viewport)
        OreDeposit.__init__(self, quantity)
