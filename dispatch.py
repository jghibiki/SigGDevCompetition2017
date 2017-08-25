import random
import math

import pygame
from pygame.locals import *

import config
from item_types import *
from items import *
from areas import *

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

        if keys[K_w]:
            # adds a new stone wall
            for y in range(0, config.world_size[0]):
                for x in range(0, config.world_size[0]):
                    if self.viewport.map_layer[y][x].mouse_collide() and self.viewport.item_layer[y][x] == None:
                        bm = BuildingMarker(x, y, self.viewport, StoneWall, [ [Stone, 50]])
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


        # add new tasks for newly selected items
        items_with_tasks = [ task.target for task in self.tasks if task.target in selected_items ]
        items_with_assigned_tasks = [ task.target for task in self.assigned_tasks if task.target in selected_items ]
        for item in selected_items:
            if isinstance(item, HoldableItemSource):
                if item not in items_with_tasks and item not in items_with_assigned_tasks:
                    self.tasks.append( GatherItemTask(item, self) )
            else:
                pass

        ## add new tasks for items on ground
        #for y in range(0, config.world_size[1]):
        #    for x in range(0, config.world_size[0]):
        #        item = self.viewport.item_layer[y][x]

        #        if isinstance(item, list):
        #            pile = item
        #            for item in pile:
        #                if isinstance(item, HoldableItem):
        #                    already_has_task = False
        #                    for task in self.tasks:
        #                        if isinstance(task, PickUpLooseItemTask) and task.target == item:
        #                            already_has_task = True
        #                            break

        #                    if not already_has_task:
        #                        for task in self.assigned_tasks:
        #                            if isinstance(task, PickUpLooseItemTask) and task.target == item:
        #                                already_has_task = True
        #                                break

        #                    if not already_has_task:
        #                        print("adding item pickup task", item)
        #                        self.tasks.append( PickUpLooseItemTask(item, self) )

        #        else:
        #            if isinstance(item, HoldableItem):
        #                already_has_task = False
        #                for task in self.tasks:
        #                    if isinstance(task, PickUpLooseItemTask) and task.target == item:
        #                        already_has_task = True
        #                        break

        #                if not already_has_task:
        #                    for task in self.assigned_tasks:
        #                        if isinstance(task, PickUpLooseItemTask) and task.target == item:
        #                            already_has_task = True
        #                            break

        #                if not already_has_task:
        #                    print("adding item pickup task", item)
        #                    self.tasks.append( PickUpLooseItemTask(item, self) )



        random.shuffle(self.units)
        for unit in self.units:
            if not unit.task:
                if len(self.tasks) > 0:
                    mapping = [ [task.distance_to_target((unit.x, unit.y)), task] for task in self.tasks ]

                    closest = min(mapping, key=lambda x: abs(x[0][0]) + abs(x[0][1] + (-5)*x[1].priority))[1]

                    self.tasks.remove(closest)
                    unit.task = closest
                    self.assigned_tasks.append(unit.task)
                    unit.update()
                else:
                    #if no tasks availiable make the unit wander
                    task = WanderingTask(unit, self)
                    unit.task = task
                    unit.update()


            elif unit.task:
                if isinstance(unit.task.target, Item):
                    if not unit.task.target.selected and unit.task.target.targetable:
                        # if the item has been unselected, abandon the task don't abandon if the task can't be targeted
                        unit.task.canceled()
                        unit.task = None
                    else:
                        unit.update()
                else:
                    unit.update()

    def queue_task(self, task):
        self.tasks.append(task)





class Task:
    def __init__(self, target, dispatcher, description):
        self.target = target
        self.dispatcher = dispatcher
        self.done = False
        self.aborted = False
        self.description = description #TODO allow for descriptions of tasks with multiple stages.
        self.priority = 0
        self.assignee = None

    def assined(self, assignee):
        self.assignee = assignee

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
        if hasattr(self.target, "viewport"):
            self.target.viewport.dirty = 1

    def postpone(self, reason=None):
        if reason:
            self.dispatcher.viewport.hud.add_alert(reason)

        self.end_task()

        self.priority -= 2

        if self not in self.dispatcher.tasks:
            self.dispatcher.tasks.append(self)



class GatherItemTask(Task):
    def __init__(self, target, dispatcher):
        Task.__init__(self, target, dispatcher, "Gathering item from item source") # TODO update description to be more detailed

    def do(self):
        # TODO: allow collection rate to scale
        collected = self.target.collect()
        if collected is None:
            self.done = True
            self.end_task()
        return collected

    def end_task(self):
        Task.end_task(self)
        if isinstance(self.target, Item):
            self.target.selected = False


class BuildBuildingTask(Task):
    def __init__(self, target, dispatcher):
        Task.__init__(self, target, dispatcher, "Building building.") #TODO update description to be more detailed.

    def do(self, material=None):
        if material:
            self.target.build(material)

        req = self.target.get_required()
        if len(req) == 0:
            self.done = True
            self.end_task()

        return req


class PickUpLooseItemTask(Task):
    def __init__(self, target, dispatcher):
        Task.__init__(self, target, dispatcher, "Getting an item off the ground.") #TODO update description to be more detailed.

        self.priority = -2

    def do(self):

        self.target.clear()
        self.target.dirty = 1
        self.dispatcher.viewport.dirty = 1

        if isinstance(self.dispatcher.viewport.item_layer[self.target.y][self.target.x], list):
            if self.target in self.dispatcher.viewport.item_layer[self.target.y][self.target.x]:
                self.dispatcher.viewport.item_layer[self.target.y][self.target.x].remove(self.target)

                for item in self.dispatcher.viewport.item_layer[self.target.y][self.target.x]:
                    item.dirty = True
        else:
            self.dispatcher.viewport.item_layer[self.target.y][self.target.x] = None

        self.done = True
        self.end_task()

        return self.target

class IdleTask(Task):
    def __init__(self, target, dispatcher, description):
        Task.__init__(self, target, dispatcher, description)

    def do(self):
        self.done = True
        self.end_task()

        return self.target

    def postpone(self, reason):
        self.done = True
        self.end_task()

class WanderingTask(IdleTask):
    def __init__(self, unit, dispatcher):
        if MeetingArea.instance:
            xy = random.choice(MeetingArea.instance.coordinates)
        else:
            mean_x = sum([ u.x for u in dispatcher.units ]) / len(dispatcher.units)
            mean_y = sum([ u.y for u in dispatcher.units ]) / len(dispatcher.units)

            mean_x = math.floor(mean_x)
            mean_y = math.floor(mean_y)

            viable_coords = []
            for x in range(random.randint(-15, -10), random.randint(10, 15)):
                for y in range(random.randint(-15, -10), random.randint(10, 15)):
                    _x = x + mean_x
                    if _x > 0 and _x < config.world_size[0]:
                        _y = y + mean_y
                        if _y > 0 and _y < config.world_size[1]:
                            viable_coords.append([ _x, _y ])

            xy = random.choice(viable_coords)


        target = GenericTarget(*xy)
        IdleTask.__init__(self, target, dispatcher, "Wandering.")
        self.priority = -99





class GenericTarget:
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.rect = pygame.Rect(x * config.image_size[0], y * config.image_size[1], 0, 0)


