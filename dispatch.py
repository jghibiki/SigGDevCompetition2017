import pygame

import config
from item_types import *
from items import *

class Dispatcher:

    def __init__(self, viewport):
        self.viewport = viewport
        self.units = []

        self.tasks = []

        self.assigned_tasks = []


    def update(self):
        selected_items = []

        for y in range(0, config.world_size[0]):
            for x in range(0, config.world_size[0]):
                item = self.viewport.item_layer[y][x]
                if (item is not None and
                    item.selected):

                    check = [ True if task.target == item else False for task in self.assigned_tasks ]

                    if check.count(True) == 0:
                        selected_items.append( item )

        for unit in self.units:
            if not unit.task:
                if len(self.tasks) > 0:
                    unit.task = self.tasks.pop()
                    self.assigned_tasks.append(unit.task)
                    unit.update()
                else:
                    if len(selected_items) > 0:
                        task_target = selected_items.pop()

                        if isinstance(task_target, HoldableItemSource):
                            unit.task = GatherItemTask(task_target)
                        else:
                            unit.task = Task(task_target)

                        self.assigned_tasks.append(unit.task)

            elif unit.task:
                if isinstance(unit.task.target, Item):
                    if not unit.task.target.selected:  # if the item has been unselected, abandon the task
                        unit.task = None
                    else:
                        unit.update()
                else:
                    unit.update()





class Task:
    def __init__(self, target):
        self.target = target
        self.done = False

    def distance_to_target(self, pos):
        return ( self.target.x - pos[0], self.target.y - pos[1] )

    def do(self):
        pass




class GatherItemTask(Task):
    def __init__(self, target):
        Task.__init__(self, target)

    def do(self):
        # TODO: allow collection rate to scale
        collected = self.target.collect()
        if not collected:
            self.done = True
        return collected



class GenericTarget:
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.rect = pygame.Rect(x * config.image_size[0], y * config.image_size[1], 0, 0)

