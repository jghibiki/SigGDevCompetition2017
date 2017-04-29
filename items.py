import pygame

import config
from item_types import *

class Grass(Block):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/grass.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y):
        Block.__init__(self, x, y, Grass.image)


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
        cls.image = pygame.image.load("assets/coal_deposit.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, CoalDeposit.image, viewport)
        OreDeposit.__init__(self, quantity)


class StoneDeposit(Item, OreDeposit):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone_deposit.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, StoneDeposit.image, viewport)
        OreDeposit.__init__(self, quantity)


class Dirt(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/dirt.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, Dirt.image, viewport)


class Tree(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/tree.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Tree.image, viewport)


class Coal(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/coal.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Coal.image, viewport)

class Furnace(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/furnace.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Furnace.image, viewport)


class ScienceStation(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/science_station.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, ScienceStation.image, viewport)


class Printer(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/science_station.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Printer.image, viewport)



class WoodenWall(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/wooden_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, WoodenWall.image, viewport)

class IronWall(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/iron_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, IronWall.image, viewport)

class CopperWall(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/copper_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, CopperWall.image, viewport)


class StoneWall(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, StoneWall.image, viewport)
