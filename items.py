import pygame

import config
from item_types import *

class Coal(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/coal.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, x, y, Coal.image, viewport)


class Stone(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, x, y, Stone.image, viewport)

class Iron(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/iron.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, x, y, Iron.image, viewport)

class Copper(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/copper.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, x, y, Copper.image, viewport)


class Grass(Block):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/grass.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y):
        Block.__init__(self, x, y, Grass.image)


class CopperOreDeposit(Item, HoldableItemSource):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/copper_ore.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, CopperOreDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Copper)



class IronOreDeposit(Item, HoldableItemSource):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/iron_ore.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity = 100):
        Item.__init__(self, x, y, IronOreDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Iron)


class CoalDeposit(Item, HoldableItemSource):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/coal_deposit.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, CoalDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Coal)


class StoneDeposit(Item, HoldableItemSource):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone_deposit.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, Stone, quantity=100):
        Item.__init__(self, x, y, StoneDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Stone)


class Dirt(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/dirt.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, Dirt.image, viewport)


class Tree(Item, Collidable, HoldableItemSource):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/tree.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Tree.image, viewport)
        HoldableItemSource.__init__(self, 10, Log)



class Coal(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/coal.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, x, y, Coal.image, viewport)

class Furnace(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/furnace.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Furnace.image, viewport)


class ScienceStation(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/science_station.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, ScienceStation.image, viewport)


class Printer(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/science_station.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Printer.image, viewport)

class IndoctrinationChamber(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/indoctrination_chamber.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, IndoctrinationChamber.image, viewport)


class WoodenWall(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/wooden_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, WoodenWall.image, viewport)

class IronWall(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/iron_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, IronWall.image, viewport)

class CopperWall(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/copper_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, CopperWall.image, viewport)


class StoneWall(Item, Collidable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, StoneWall.image, viewport)

class Log(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/log.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, x, y, Log.image, viewport)


