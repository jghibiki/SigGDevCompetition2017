import pygame

import config
from block import Block

class Collidable():
    pass


class Item(Block):

    def __init__(self, x, y, image, viewport, targetable=True, hoverable=True):
        Block.__init__(self, x, y, image, viewport)

        self.targetable = targetable
        self.hoverable = targetable or hoverable

        self.collided = False

        self.selected = False

    def mouse_collide(self, pos=None, side_effect=True):
        rect = self.image.get_rect()
        rect = pygame.Rect(
                self.x * config.image_size[0],
                self.y * config.image_size[1],
                config.image_size[0],
                config.image_size[1])

        if not pos:
            pos = pygame.mouse.get_pos()

        corrected_pos = ( pos[0] + self.viewport.v_rect.x, pos[1] + self.viewport.v_rect.y )

        collided = rect.collidepoint(corrected_pos)

        previously_collided = self.collided
        self.collided = collided

        if (self.targetable or self.hoverable) and side_effect:
            if ( (not previously_collided and collided) or
                 (previously_collided and not collided) ):
                self.dirty = 1
                self.viewport.dirty = 1

        return collided

    def toggle_selected(self):
        if self.targetable:
            self.selected = not self.selected
            self.dirty = 1
            self.viewport.dirty = 1

    def clear(self):
        self.viewport.item_layer_surf.fill(pygame.Color(0, 0, 0, 1), rect=(
            self.x * config.image_size[0],
            self.y * config.image_size[1],
            config.image_size[0], config.image_size[1] ))

    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2 or force:
            if self.dirty == 1:
                self.dirty = 0

            self.clear()

            if self.collided and not self.selected:
                b = config.selection_border
                cpy = self.image.copy()
                cpy.fill(pygame.Color("#FF0000"), rect=(0, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#FF0000"), rect=(config.image_size[0] - b, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#FF0000"), rect=(0, 0, config.image_size[1], b))
                cpy.fill(pygame.Color("#FF0000"), rect=(0, config.image_size[0] - b, config.image_size[1], b))

                surf.blit(cpy, (self.rect.x, self.rect.y))

            elif self.selected and not self.collided:
                b = config.selection_border
                cpy = self.image.copy()
                cpy.fill(pygame.Color("#FFFFFF"), rect=(0, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#FFFFFF"), rect=(config.image_size[0] - b, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#FFFFFF"), rect=(0, 0, config.image_size[1], b))
                cpy.fill(pygame.Color("#FFFFFF"), rect=(0, config.image_size[0] - b, config.image_size[1], b))

                surf.blit(cpy, (self.rect.x, self.rect.y))

            elif self.selected and self.collided:
                b = config.selection_border
                cpy = self.image.copy()
                cpy.fill(pygame.Color("#888888"), rect=(0, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#888888"), rect=(config.image_size[0] - b, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#888888"), rect=(0, 0, config.image_size[1], b))
                cpy.fill(pygame.Color("#888888"), rect=(0, config.image_size[0] - b, config.image_size[1], b))

                surf.blit(cpy, (self.rect.x, self.rect.y))

            else:
                return surf.blit(self.image, (self.rect.x, self.rect.y))

class HoldableItem(Item):
    def __init__(self, name, x, y, image, viewport):
        Item.__init__(self, x, y, image, viewport, targetable=False)
        self.name = name

    def set_location(self, x, y):
        self.x = x
        self.y = y

        self.rect = self.image.get_rect().move(
                x * config.image_size[0],
                y * config.image_size[1])


    def __str__(self):
        return self.name



class HoldableItemSource():
    def __init__(self, quantity, item_factory, collection_rate=1, gather_time=2):
        self.quantity = quantity
        self.item_factory = item_factory
        self.exhausted = False
        self.collection_rate = collection_rate
        self.gather_time = gather_time
        self.gather_counter = 0

    def collect(self, max_collection=None):
        #TODO find some sort of scailing collection rate
        if not self.exhausted:
            if self.gather_counter < self.gather_time:
                self.gather_counter += 1
                return []
            else:
                self.gather_counter = 0

                if max_collection:
                    collect = min(max_collection, self.collection_rate)
                else:
                    collect = self.collection_rate

                if self.quantity - collect >= 0:
                    self.quantity -= collect
                    if self.quantity == 0:

                        #remove self from item layer
                        self.clear()
                        self.viewport.item_layer[self.y][self.x] = None
                        self.dirty = 1
                        self.viewport.dirty = 1

                    return [ self.item_factory(0, 0, self.viewport) for _ in range(0, collect) ]
                #TODO there is a missing case here figure it out

                else:
                    return None
        return None

    def remaining(self):
        return self.quantity



class Container(Item):

    def __init__(self, capacity, x, y, image, viewport):
        Item.__init__(self, x, y, image, viewport, targetable=False)

        self.capacity = capacity
        self.items = []


    def can_store(self):
        return len(self.items) < self.capacity

    def store(self, item):
        self.items.append(item)

    def check_for_item(self, type_of_item):
        for item in self.items:
            if isinstance(item, type_of_item):
                return True
        return False

    def retrieve(self, type_of_item):
        for item in self.items:
            if isinstance(item, type_of_item):
                self.items.remove(item)
                return item

class Buildable(Item, Collidable):
    def __init__(self, name, x, y, image, viewport):
        Item.__init__(self, x, y, image, viewport)
        self.name = name


class BuildingPlaceholder:
    def __init__(self, type_factory, requirements):
        self.requirements  = [ {"type": req[0], "needed": req[1], "collected": 0} for req in requirements ]
        self.built = False
        self.type_factory = type_factory

    def build(self, material):
        for req in self.requirements:
            if req["type"] == type(material):
                req["collected"] += 1
        if len(self.get_required()) == 0:
            # nothing left to fetch, replace with build object
            self.built = True
            self.viewport.item_layer[self.y][self.x] = self.type_factory(self.x, self.y, self.viewport)
            self.viewport.dirty = True
            self.dirty = 1

    def get_required(self):
        reqs = []
        for req in self.requirements:
            if req["collected"] < req["needed"]:
                reqs.append( ( req["type"], req["needed"] - req["collected"]) )
        return reqs



