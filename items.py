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
        cls.image = pygame.image.load("assets/sci_fi_grass.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Block.__init__(self, x, y, Grass.image, viewport)


class CopperOreDeposit(Item, HoldableItemSource, Collidable):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/crystal_deposits/yellow.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, CopperOreDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Copper)



class IronOreDeposit(Item, HoldableItemSource, Collidable):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/crystal_deposits/red.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity = 100):
        Item.__init__(self, x, y, IronOreDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Iron)


class CoalDeposit(Item, HoldableItemSource, Collidable):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/crystal_deposits/purple.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, CoalDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Coal)


class StoneDeposit(Item, HoldableItemSource, Collidable):

    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone_alt.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, StoneDeposit.image, viewport)
        HoldableItemSource.__init__(self, quantity, Stone, gather_time=5)


class Dirt(Item):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/dirt.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, quantity=100):
        Item.__init__(self, x, y, Dirt.image, viewport)

class IronWall(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/iron_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Buildable.__init__(self, x, y, IronWall.image, viewport)

class StoneWall(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/stone_wall.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Buildable.__init__(self, x, y, StoneWall.image, viewport)

class Stockpile(Container):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/crate.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Container.__init__(self, 500, x, y, Stockpile.image, viewport)


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
        cls.image = pygame.image.load("assets/printer.png")
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

class DeliveryBot(Buildable):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/delivery_bot.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport):
        Item.__init__(self, x, y, DeliveryBot.image, viewport)

class BuildingMarker(Item, Collidable, BuildingPlaceholder):
    @classmethod
    def load_images(cls):
        cls.image = pygame.image.load("assets/building_marker.png")
        cls.image = pygame.transform.scale(cls.image, config.image_size)

    def __init__(self, x, y, viewport, type_factory, requirements):
        Item.__init__(self, x, y, BuildingMarker.image, viewport, False)
        BuildingPlaceholder.__init__(self, type_factory, requirements)
