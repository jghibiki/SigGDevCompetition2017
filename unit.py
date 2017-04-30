from uuid import uuid4
import random

import pygame

import config
from block import Block
from item_types import *

class Unit(Block):
    @classmethod
    def load_images(cls):
        cls.images = [
                pygame.image.load("assets/character_1.png"),
                pygame.image.load("assets/character_2.png"),
                pygame.image.load("assets/character_1.png"),

                pygame.transform.flip(pygame.image.load("assets/character_2.png"), True, False),
                pygame.transform.flip(pygame.image.load("assets/character_3.png"), True, False),
                pygame.transform.flip(pygame.image.load("assets/character_3.png"), True, False)
        ]
        for i in range(0, len(cls.images)):
            cls.images[i] = pygame.transform.scale(cls.images[i], config.image_size)

    def __init__(self, x, y, viewport, dispatcher):
        self.viewport = viewport
        self.dispatcher = dispatcher

        self.old_x = x
        self.old_y = y

        self.inventory = []

        self.id = str(uuid4())

        image = random.choice(Unit.images)
        Block.__init__(self, x, y, image)

        self.task = None

    def update(self):
        if self.task:
            distance_to_task = self.task.distance_to_target((self.x, self.y))
            if distance_to_task[0] == 1 and distance_to_task[1] == 1:
                result = self.task.do()
                if result:
                    self.inventory = self.inventory + result
                if self.task.done:
                    self.task = None
            else:
                self.old_x = self.x
                self.old_y = self.y

                stuck = True
                # TODO: Track the location where we were stuck at as well as which unstuck options we have tried,
                #       don't retry an option. reset stuck state if we move more than 2 squares away from stuck location

                if distance_to_task[0] > 1:
                    if self.check_collision(self.x+1, self.y):
                        self.x += 1
                        self.rect.x += config.image_size[0]
                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

                if distance_to_task[0] < 1:
                    if self.check_collision(self.x-1, self.y):
                        self.x -= 1
                        self.rect.x -= config.image_size[0]
                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

                if distance_to_task[1] > 1:
                    if self.check_collision(self.x, self.y+1):
                        self.y += 1
                        self.rect.y += config.image_size[1]
                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

                if distance_to_task[1] < 1:
                    if self.check_collision(self.x, self.y-1):
                        self.y -= 1
                        self.rect.y -= config.image_size[1]
                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

                if stuck and abs(distance_to_task[0]) > 1 and abs(distance_to_task[1]) > 1:
                    option = random.randint(1, 4)
                    if (option == 1 and
                        self.check_collision(self.y-1, self.x-1)):

                        self.x -= 1
                        self.rect.x -= config.image_size[0]

                        self.y -= 1
                        self.rect.y -= config.image_size[1]

                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

                    elif (option == 2 and
                          self.check_collision(self.x-1, self.y+1)):

                        self.x -= 1
                        self.rect.x -= config.image_size[0]

                        self.y += 1
                        self.rect.y += config.image_size[1]

                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

                    elif (option == 3 and
                          self.check_collision(self.x+1, self.y+1)):

                        self.x += 1
                        self.rect.x += config.image_size[0]

                        self.y += 1
                        self.rect.y += config.image_size[1]

                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

                    elif (option == 4 and self.check_collision(self.x+1, self.y-1)):

                        self.x += 1
                        self.rect.x += config.image_size[0]

                        self.y -= 1
                        self.rect.y -= config.image_size[1]

                        self.dirty = 1
                        self.viewport.dirty = 1
                        stuck = False

    def check_collision(self, x, y):

        if x < 0 or y < 0:
            return False

        if x >= config.world_size[0] or y >= config.world_size[1]:
            return False

        item = self.viewport.item_layer[y][x]
        if item != None and isinstance(item, Collidable):
            return False

        for unit in self.dispatcher.units:
            if unit.x == x and unit.y == y:
                return False

        return True


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2 or force:
            if self.dirty == 1:
                self.dirty = 0

            surf.fill(pygame.Color(0, 0, 0, 1), rect=(
                self.old_x * config.image_size[0],
                self.old_y * config.image_size[1],
                config.image_size[0], config.image_size[1] ))

            return surf.blit(self.image, (self.rect.x, self.rect.y))
