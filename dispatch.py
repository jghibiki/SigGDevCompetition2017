import random

import pygame
from pygame.locals import *

import config
from item_types import *
from items import *

class Dispatcher:

    def __init__(self, viewport):
        self.viewport = viewport
        self.units = []

        self.tasks = []

        self.assigned_tasks = []

        self.stock_piles = []

    def handle_keyboard_events(self):
        keys = pygame.key.get_pressed()

        if keys[K_s]:

            # adds a new stockpile
            for y in range(0, config.world_size[0]):
                for x in range(0, config.world_size[0]):
                    if self.viewport.map_layer[y][x].mouse_collide() and self.viewport.item_layer[y][x] == None:
                        sp = Stockpile(x, y, self.viewport)
                        self.stock_piles.append( sp )
                        self.viewport.item_layer[y][x] = sp
                        self.viewport.dirty = 1
                        break
                else:
                    continue
                break

        if keys[K_f]:

            # adds a new stockpile
            for y in range(0, config.world_size[0]):
                for x in range(0, config.world_size[0]):
                    if self.viewport.map_layer[y][x].mouse_collide() and self.viewport.item_layer[y][x] == None:
                        bm = BuildingMarker(x, y, self.viewport, Furnace, [ [Stone, 100], [Wood, 200] ])
                        self.tasks.append( BuildBuildingTask( bm, self ) )
                        self.viewport.item_layer[y][x] = bm
                        self.viewport.dirty = 1
                        break



    def update(self):
        selected_items = []

        for y in range(0, config.world_size[0]):
            for x in range(0, config.world_size[0]):
                item = self.viewport.item_layer[y][x]
                if item is not None:

                    if isinstance(item, list):
                        item_list = item
                        for item in item_list:
                            if item.selected:
                                check = [ True if task.target == item else False for task in self.assigned_tasks ]
                                if check.count(True) == 0:
                                    selected_items.append( item )


                    else:
                        if item.selected:
                            check = [ True if task.target == item else False for task in self.assigned_tasks ]
                            if check.count(True) == 0:
                                selected_items.append( item )

        random.shuffle(self.units)
        for unit in self.units:
            if not unit.task:
                if len(self.tasks) > 0:
                    print("assigning task")
                    mapping = [ [task.distance_to_target((unit.x, unit.y)), task] for task in self.tasks ]
                    closest = min(mapping, key=lambda x: abs(x[0][0]) + abs(x[0][1]))[1]
                    self.tasks.remove(closest)
                    unit.task = closest
                    self.assigned_tasks.append(unit.task)
                    unit.update()
                else:
                    if len(selected_items) > 0:
                        mapping = [ [ abs(unit.x - task.x) + abs(unit.y - task.y), task] for task in selected_items ]
                        task_target = min(mapping, key=lambda x: x[0])[1]
                        selected_items.remove(task_target)

                        if isinstance(task_target, HoldableItemSource):
                            unit.task = GatherItemTask(task_target, self)
                        else:
                            unit.task = Task(task_target, self)

                        self.assigned_tasks.append(unit.task)

            elif unit.task:
                if isinstance(unit.task.target, Item):
                    if not unit.task.target.selected and unit.task.target.targetable:
                        # if the item has been unselected, abandon the task don't abandon if the task can't be targeted
                        unit.task.canceled()
                        unit.task = None
                    else:
                        unit.update()
                else:
                    print("work on task")
                    unit.update()





class Task:
    def __init__(self, target, dispatcher):
        self.target = target
        self.dispatcher = dispatcher
        self.done = False
        self.aborted = False

    def distance_to_target(self, pos):
        return ( self.target.x - pos[0], self.target.y - pos[1] )

    def do(self):
        pass

    def abort(self, reason=None):
        self.aborted = True
        self.end_task()
        if reason:
            self.dispatcher.viewport.hud.add_alert(reason)

    def canceled(self):
        self.end_task()
        self.done = True

    def end_task(self):
        if self in self.dispatcher.assigned_tasks:
            self.dispatcher.assigned_tasks.remove(self)
        self.target.dirty = 1
        self.target.viewport.dirty = 1


class GatherItemTask(Task):
    def __init__(self, target, dispatcher):
        Task.__init__(self, target, dispatcher)

    def do(self):
        # TODO: allow collection rate to scale
        collected = self.target.collect()
        if not collected:
            self.done = True
            self.end_task()
        return collected

    def end_task(self):
        Task.end_task(self)
        if isinstance(self.target, Item):
            self.target.selected = False


class BuildBuildingTask(Task):
    def __init__(self, target, dispatcher):
        Task.__init__(self, target, dispatcher)

    def do(self, material=None):
        if material:
            self.target.build(material)

        req = self.target.get_required()
        if len(req) == 0:
            self.done = True
            self.end_task()

        return req






class GenericTarget:
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.rect = pygame.Rect(x * config.image_size[0], y * config.image_size[1], 0, 0)

