import pygame

import config
from item_types import *

class Coal(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/coal.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, "Coal", x, y, Coal.image, viewport)


class Stone(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, "Stone",  x, y, Stone.image, viewport)

class Iron(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/iron.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, "Iron", x, y, Iron.image, viewport)

class Copper(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/copper.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, "Copper", x, y, Copper.image, viewport)


class Grass(Block):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/grass.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Block.__init__(self, x, y, Grass.image, viewport)


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

    def __init__(self, x, y, viewport, quantity=100):
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
        HoldableItemSource.__init__(self, 10, Wood)



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

class Wood(HoldableItem):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/log.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        HoldableItem.__init__(self, "Wood", x, y, Wood.image, viewport)

class Stockpile(Container):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/crate.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Container.__init__(self, 50, x, y, Stockpile.image, viewport)


class ReanimationChamber(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/reanimation_chamber.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, ReanimationChamber.image, viewport)


class Furnace(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/furnace.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Furnace.image, viewport)


class ScienceStation(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/science_station.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, ScienceStation.image, viewport)


class Printer(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/science_station.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, Printer.image, viewport)

class IndoctrinationChamber(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/indoctrination_chamber.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, IndoctrinationChamber.image, viewport)


class BuildingMarker(Item, Collidable, BuildingPlaceholder):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/building_marker.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, type_factory, requirements):
        Item.__init__(self, x, y, BuildingMarker.image, viewport, False)
        BuildingPlaceholder.__init__(self, type_factory, requirements)
