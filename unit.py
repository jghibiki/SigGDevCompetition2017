from uuid import uuid4
import random
import math
import json

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
        image = random.choice(Unit.images)
        Block.__init__(self, x, y, image, viewport)

        self.dispatcher = dispatcher

        self.old_x = x
        self.old_y = y

        with open("names.json") as f:
            names = json.load(f)
            self.name = random.choice(names["unit_names"])

        self.cooperation_rating = 10
        self.regeneration_coefficient = random.uniform(0.2, 0.70)
        self.degeneration_coefficient = random.uniform(0.5, 1.2)


        self.stuck_options_tried = [ False, False, False, False ]
        self.stuck_location = None
        self.turns_stuck = 0

        self.stock_pile = None

        self.inventory = []
        self.inventory_size = 10

        self.id = str(uuid4())


        self.work_surf = None

        self.task = None
        self.work_target = None

        self.dirty = 2


    def update(self):

        # updating cooperation rating
        update_coop = random.random()
        regenerate = bool(random.randint(0, 1))
        if update_coop > config.unit_degeneration_change:
            if regenerate:
                if self.cooperation_rating - self.degeneration_coefficient > 0:
                    self.cooperation_rating -= self.degeneration_coefficient
            else:
                if self.cooperation_rating - self.regeneration_coefficient <= 10:
                    self.cooperation_rating += self.regeneration_coefficient


        productive = bool(random.randint(0, 1))
        if self.cooperation_rating >= 5 or ( 0 < self.cooperation_rating < 5 and productive):

            # if the task is done clear it out so we can be elidgable for another
            if self.task is not None and self.task.done:
                print("task finished")
                self.task = None
                self.dirty = 1
                self.viewport.dirty = 1 # refresh screen to remove line
                return

            if len(self.inventory) >= self.inventory_size:
                # inventory is full, we need to drop stuff off at a stockpile

                if self.stock_pile is None: # we have no selected stock pile fint closest one
                    mapping = [ [ abs(stock_pile.x - self.x) + abs(stock_pile.y - self.y), stock_pile ] for stock_pile in self.dispatcher.stock_piles if stock_pile.can_store() ]

                    if len(mapping) > 0:
                        closest = min(mapping, key=lambda x: x[0])[1]
                        self.stock_pile = closest
                        return
                    else:

                        # if we get here there were no valid stock piles so we will just drop everything on the ground
                        for item in self.inventory:
                            item.set_location(self.x, self.y)
                            item.dirty = 1

                        self.viewport.item_layer[self.y][self.x] = self.inventory[:]
                        self.viewport.dirty = 1
                        self.dirty = 1

                        self.inventory = []

                else: # there is a stockpile that is availiable

                    if self.turns_stuck >= 5: # we got stuck
                        self.viewport.hud.add_alert("{0} canceled store item in stockpile. Reason: could not find a clear path.".format(self.name))

                        # we will just dump inventory on ground
                        for item in self.inventory:
                            item.set_location(self.x, self.y)
                            item.dirty = 1

                        self.viewport.item_layer[self.y][self.x] = self.inventory[:]
                        self.viewport.dirty = 1
                        self.dirty = 1

                        self.inventory = []

                        return

                    else:
                        distance_to = (self.stock_pile.x - self.x, self.stock_pile.y - self.y)
                        if (abs(distance_to[0]) == 1 and abs(distance_to[1]) == 0 or
                            abs(distance_to[0]) == 0 and abs(distance_to[1]) == 1 or
                            abs(distance_to[0]) == 1 and abs(distance_to[1]) == 1):

                            while self.stock_pile.can_store() and len(self.inventory) > 0:

                                item = self.inventory.pop()
                                self.stock_pile.store(item)

                            self.stock_pile = None

                        else:
                            # try to path to stock pile
                            self.old_x = self.x
                            self.old_y = self.y
                            self.path_to(distance_to)

            elif self.task:

                if isinstance(self.task.target, Item) and not self.task.target.selected:
                    self.task.canceled()
                    self.task = None
                    return

                # abort if we have been stuck for 5 ticks
                if self.turns_stuck >= 5:
                    self.task.abort(reason="{0} aborted task. Reason: could not find a clear path.".format(self.name))
                    self.task = None
                    self.turns_stuck = 0
                    return


                distance_to_task = self.task.distance_to_target((self.x, self.y))
                if (abs(distance_to_task[0]) == 1 and abs(distance_to_task[1]) == 0 or
                    abs(distance_to_task[0]) == 0 and abs(distance_to_task[1]) == 1 or
                    abs(distance_to_task[0]) == 1 and abs(distance_to_task[1]) == 1):
                    self.do_task()

                else:
                    self.old_x = self.x
                    self.old_y = self.y
                    self.path_to(distance_to_task)

    def do_task(self):
        # set work target
        self.work_target = (self.task.target.x * config.image_size[0], self.task.target.y * config.image_size[1])
        self.dirty = 1
        self.viewport.dirty = 1

        # work on task
        result = self.task.do()
        if result:
            self.inventory.extend(result)

    def check_collision(self, x, y):

        if x < 0 or y < 0:
            return True

        if x >= config.world_size[0] or y >= config.world_size[1]:
            return Truee

        item = self.viewport.item_layer[y][x]
        if item != None and isinstance(item, Collidable):
            return True

        #for unit in self.dispatcher.units:
        #    if unit.x == x and unit.y == y:
        #        return True

        return False


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2 or force or self.work_target is not None:
            if self.dirty == 1:
                self.dirty = 0

            surf.fill(pygame.Color(0, 0, 0, 1), rect=(
                self.old_x * config.image_size[0],
                self.old_y * config.image_size[1],
                config.image_size[0], config.image_size[1] ))

            return surf.blit(self.image, (self.rect.x, self.rect.y))

    def draw_action(self, surf, force=False):
        if self.work_target is not None:
            rects = pygame.draw.line(surf, pygame.Color("#FF0000"),
                    (self.x * config.image_size[0] + math.floor(config.image_size[0]/2),
                     self.y * config.image_size[1] + math.floor(config.image_size[0]/2)),
                    (self.work_target[0] + math.floor(config.image_size[0]/2),
                      self.work_target[1] + math.floor(config.image_size[0]/2)) , 4)
            self.work_target = None


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


    def path_to(self, distance_to):
        stuck = True

        if distance_to[0] > 0:
            if not self.check_collision(self.x+1, self.y):
                self.x += 1
                self.rect.x += config.image_size[0]
                self.dirty = 1
                self.viewport.dirty = 1
                stuck = False
                self.turns_stuck = 0

        if distance_to[0] < 0:
            if not self.check_collision(self.x-1, self.y):
                self.x -= 1
                self.rect.x -= config.image_size[0]
                self.dirty = 1
                self.viewport.dirty = 1
                stuck = False
                self.turns_stuck = 0

        if distance_to[1] > 0:
            if not self.check_collision(self.x, self.y+1):
                self.y += 1
                self.rect.y += config.image_size[1]
                self.dirty = 1
                self.viewport.dirty = 1
                stuck = False
                self.turns_stuck = 0

        if distance_to[1] < 0:
            if not self.check_collision(self.x, self.y-1):
                self.y -= 1
                self.rect.y -= config.image_size[1]
                self.dirty = 1
                self.viewport.dirty = 1
                stuck = False
                self.turns_stuck = 0

        if stuck and ( abs(distance_to[0]) > 0 or abs(distance_to[1]) > 0 ):

            self.turns_stuck += 1

            if self.stuck_location is None:
                self.stuck_location = (self.x , self.y)

            if abs(self.stuck_location[0] - self.x ) > 2 and abs(self.stuck_location[1] - self.y):
                print("unstuck")
                self.stuck_location = None
                self.stuck_options_tried = [ False, False, False, False ]
                self.turns_stuck = 0


            if not self.stuck_options_tried[0]:
                print("tried option 1")

                self.stuck_options_tried[0] = True

                if not self.check_collision(self.y-1, self.x-1):
                    print("option 1")
                    self.x -= 1
                    self.rect.x -= config.image_size[0]

                    self.y -= 1
                    self.rect.y -= config.image_size[1]

                    self.dirty = 1
                    self.viewport.dirty = 1
                    stuck = False

            elif not self.stuck_options_tried[1]:
                print("tried option 2")

                self.stuck_options_tried[1] = True

                if not self.check_collision(self.x-1, self.y+1):
                    print("option 2")
                    self.x -= 1
                    self.rect.x -= config.image_size[0]

                    self.y += 1
                    self.rect.y += config.image_size[1]

                    self.dirty = 1
                    self.viewport.dirty = 1
                    stuck = False

            elif not self.stuck_options_tried[2]:
                self.stuck_options_tried[2] = True
                print("tried option 3")

                if not self.check_collision(self.x+1, self.y+1):
                    print("option 3")
                    self.x += 1
                    self.rect.x += config.image_size[0]

                    self.y += 1
                    self.rect.y += config.image_size[1]

                    self.dirty = 1
                    self.viewport.dirty = 1
                    stuck = False

            elif not self.stuck_options_tried[3]:
                self.stuck_options_tried[3] = True
                print("tried option 4")

                if not self.check_collision(self.x+1, self.y-1):
                    print("option 4")

                    self.x += 1
                    self.rect.x += config.image_size[0]

                    self.y -= 1
                    self.rect.y -= config.image_size[1]

                    self.dirty = 1
                    self.viewport.dirty = 1
                    stuck = False

    def check_collision(self, x, y):

        if x < 0 or y < 0:
            return True

        if x >= config.world_size[0] or y >= config.world_size[1]:
            return Truee

        item = self.viewport.item_layer[y][x]
        if item != None and isinstance(item, Collidable):
            return True

        #for unit in self.dispatcher.units:
        #    if unit.x == x and unit.y == y:
        #        return True

        return False


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2 or force or self.work_target is not None:
            if self.dirty == 1:
                self.dirty = 0

            surf.fill(pygame.Color(0, 0, 0, 1), rect=(
                self.old_x * config.image_size[0],
                self.old_y * config.image_size[1],
                config.image_size[0], config.image_size[1] ))

            return surf.blit(self.image, (self.rect.x, self.rect.y))

    def draw_action(self, surf, force=False):
        if self.work_target is not None:
            rects = pygame.draw.line(surf, pygame.Color("#FF0000"),
                    (self.x * config.image_size[0] + math.floor(config.image_size[0]/2),
                     self.y * config.image_size[1] + math.floor(config.image_size[0]/2)),
                    (self.work_target[0] + math.floor(config.image_size[0]/2),
                      self.work_target[1] + math.floor(config.image_size[0]/2)) , 4)
            self.work_target = None


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

