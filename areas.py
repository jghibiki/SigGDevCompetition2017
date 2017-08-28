import math

import pygame

import config

class Area:
    def __init__(self, coordinates, name, color):
        self.added = coordinates
        self.coordinates = list(coordinates)
        self.removed = []

        self.name = name
        self.color = pygame.Color(color)
        self.color.a = math.floor(255 * .10)
        self.surf = pygame.Surface((config.image_size[0] * config.world_size[0], config.image_size[1] * config.world_size[1]), flags=pygame.SRCALPHA)
        self.dirty = 1

        self.tile = pygame.Surface(config.image_size, flags=pygame.SRCALPHA)
        self.tile.fill(self.color)

    def update(self):

        for c in self.added:
            self.surf.blit(self.tile, (c[0] * config.image_size[0], c[1] * config.image_size[1]))
            self.dirty = 1
        self.added = []

        for c in self.removed:
            r = [ c[0], c[1], config.image_size, config.image_size ]
            self.surf.fill(pygame.Color(0, 0, 0, 1), r)
            self.dirty = 1
        self.remove = []


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2 or force:
            if self.dirty == 1:
                self.dirty = 0
            return surf.blit(self.surf, (0, 0))



class MeetingArea(Area):
    instance = None
    def __init__(self, coordinates, name="Meeting Area"):
        Area.__init__(self, coordinates, name, color="#ffffff")
        MeetingArea.instance = self

