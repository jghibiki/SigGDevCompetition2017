from uuid import uuid4
import random
import math
import json

import pygame

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import config
from block import Block
from item_types import *
from dispatch import *

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
        self.collection_target = None
        self.return_from_collection = False

        self.dirty = 1


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
                self.task = None
                self.dirty = 1
                self.viewport.dirty = 1 # refresh screen to remove line
                return

            if self.collection_target is not None:
                mapping = []
                for stock_pile in self.dispatcher.stock_piles:
                    random.shuffle(self.collection_target)
                    if stock_pile.check_for_item(self.collection_target[0][0]):
                        mapping.append( [ abs(stock_pile.x - self.x) + abs(stock_pile.y - self.y), stock_pile ] )

                if len(mapping) > 0:
                    print("closest stock pile")
                    closest = min(mapping, key=lambda x: x[0])[1]
                    distance_to = (closest.x - self.x, closest.y - self.y)
                    if (abs(distance_to[0]) == 1 and abs(distance_to[1]) == 0 or
                        abs(distance_to[0]) == 0 and abs(distance_to[1]) == 1 or
                        abs(distance_to[0]) == 1 and abs(distance_to[1]) == 1 or
                        abs(distance_to[0]) == 0 and abs(distance_to[1]) == 0):

                        print("collecting...")

                        valid_item = True
                        while len(self.inventory) < self.inventory_size and valid_item:
                            item = closest.retrieve( self.collection_target[0][0] )
                            if item != None:
                                print("got item", item)
                                self.inventory.append(item)
                            else:
                                print("invalid item")
                                valid_item = False

                        self.collection_target = None

                    else:
                        # try to path to stock pile
                        print("pathing to")
                        self.old_x = self.x
                        self.old_y = self.y
                        self.path_to((closest.x, closest.y))
                else:
                    # not enough supplies availiable try again later
                    print("postponing")
                    self.task.postpone("{0} postponing construction task. Reason: Failed to find stockpile with required building materials.".format(self.name))
                    self.task = None
                    self.collection_target = None



            elif len(self.inventory) >= self.inventory_size and not isinstance(self.task, BuildBuildingTask):
                # inventory is full, we need to drop stuff off at a stockpile, but don't if we have a task
                # as we may be getting stuff

                if self.stock_pile is None: # we have no selected stock pile fint closest one
                    mapping = [ [ abs(stock_pile.x - self.x) + abs(stock_pile.y - self.y), stock_pile ] for stock_pile in self.dispatcher.stock_piles if stock_pile.can_store() ]

                    if len(mapping) > 0:
                        closest = min(mapping, key=lambda x: x[0])[1]
                        if closest is not None:
                            print("set stockpile")
                            self.stock_pile = closest
                        return
                    else:
                        if self.task is not None:
                            self.task.postpone("{0} postponing task. Reason: Failed to find stockpile with required storage space.".format(self.name))
                            self.task = None


                else: # there is a stockpile that is availiable

                    if self.turns_stuck >= 5: # we got stuck
                        self.viewport.hud.add_alert("{0} canceled store item in stockpile. Reason: could not find a clear path.".format(self.name))
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
                            self.path_to((self.stock_pile.x, self.stock_pile.y))

            elif self.task:

                if (isinstance(self.task.target, Item)
                        and self.task.target.targetable # don't cancel if not targetable
                        and not self.task.target.selected):
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
                    result = self.path_to((self.task.target.x, self.task.target.y))
                    if not result:
                        self.task.postpone("{0} postponing task \"{1}\". Reason: Failed to find a clear path to task.".format(self.name, self.task.description))
                        self.task = None

    def do_task(self):
        # set work target
        if not isinstance(self.task, WanderingTask):
            self.work_target = (self.task.target.x * config.image_size[0], self.task.target.y * config.image_size[1])
        else: self.work_target = None

        self.dirty = 1
        self.viewport.dirty = 1

        # work on task
        if isinstance(self.task, GatherItemTask):
            if len(self.inventory) < self.inventory_size:
                result = self.task.do()
                if result is not None:
                    self.inventory.extend(result)
            else:
                self.task.postpone("{0} postponing task \"{1}\". Reason: Inventory full.".format(self.name, self.task.description))
                self.task = None

        elif isinstance(self.task, PickUpLooseItemTask):
            if len(self.inventory) < self.inventory_size:
                result = self.task.do()
                self.inventory.append(result)
                self.task = None # this task is a one-and-done

        elif isinstance(self.task, BuildBuildingTask):
            reqs = self.task.do()


            availiable_items = []
            unneeded_items = []

            for item in self.inventory:
                print(item)
                for req in reqs:
                    print(req)
                    if isinstance(item, req[0]):
                        print("needed", item)
                        availiable_items.append(item)
                    else:
                        unneeded_items.append(item)
                        print("unneeded", item)

            for item in unneeded_items:
                item.set_location(self.x, self.y)
                item.dirty = 1

            self.inventory = [ item for item in self.inventory if item not in unneeded_items ]
            self.viewport.item_layer[self.y][self.x] = unneeded_items
            self.viewport.dirty = 1
            self.dirty = 1

            self.inventory = []


            built = False
            while len(availiable_items) > 0 and not built:
                item = availiable_items.pop()
                reqs = self.task.do(item)
                if len(reqs) == 0:
                    built = True

            if not built:
                self.collection_target = reqs
            else:
                self.collection_target = None
            self.return_from_collection = False

        elif isinstance(self.task, WanderingTask):
            self.task = None




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


    def path_to(self, pos):

        matrix = []

        for y in range(0, config.world_size[1]):
            col = []
            for x in range(0, config.world_size[0]):
                if x == pos[0] and y == pos[1]:
                    collidable = 0
                else:
                    collidable = 1 if isinstance(self.viewport.item_layer[y][x], Collidable) else 0

                for unit in self.dispatcher.units:
                    if unit.x == x and unit.y == y:
                        collidable = 1

                col.append(collidable)
            matrix.append(col)

        grid = Grid(matrix=matrix)

        start = grid.node(self.x, self.y)
        end = grid.node(*pos)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)


        if len(path) > 1:
            self.x = path[1][0]
            self.rect.x = path[1][0] * config.image_size[0]

            self.y = path[1][1]
            self.rect.y = path[1][1] * config.image_size[1]

            self.dirty = 1
            self.viewport.dirty = 1

            return True
        else:
            return False


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

