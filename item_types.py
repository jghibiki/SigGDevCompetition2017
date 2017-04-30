import pygame

import config
from block import Block


class Item(Block):

    def __init__(self, x, y, image, viewport):
        Block.__init__(self, x, y, image)
        self.viewport = viewport

        self.collided = False

        self.selected = False

    def mouse_collide(self, pos=None, side_effect=True):
        rect = self.image.get_rect()
        rect = pygame.Rect(
                self.x * config.image_size[0],
                self.y * config.image_size[1],
                rect.w, rect.h)

        if not pos:
            pos = pygame.mouse.get_pos()

        corrected_pos = ( pos[0] + self.viewport.v_rect.x, pos[1] + self.viewport.v_rect.y )

        collided = rect.collidepoint(corrected_pos)

        previously_collided = self.collided
        self.collided = collided

        if side_effect:
            if ( (not previously_collided and collided) or
                 (previously_collided and not collided) ):
                self.dirty = 1
                self.viewport.dirty = 1

        return collided

    def toggle_selected(self):
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
                cpy.fill(pygame.Color("#000000"), rect=(0, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#000000"), rect=(config.image_size[0] - b, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#000000"), rect=(0, 0, config.image_size[1], b))
                cpy.fill(pygame.Color("#000000"), rect=(0, config.image_size[0] - b, config.image_size[1], b))

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
                cpy.fill(pygame.Color("#AAAAAA"), rect=(0, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#AAAAAA"), rect=(config.image_size[0] - b, 0, b, config.image_size[1]))
                cpy.fill(pygame.Color("#AAAAAA"), rect=(0, 0, config.image_size[1], b))
                cpy.fill(pygame.Color("#AAAAAA"), rect=(0, config.image_size[0] - b, config.image_size[1], b))

                surf.blit(cpy, (self.rect.x, self.rect.y))

            else:
                return surf.blit(self.image, (self.rect.x, self.rect.y))

class HoldableItem(Item):
    def __init__(self, x, y, image, viewport):
        Item.__init__(self, x, y, image, viewport)


class HoldableItemSource():
    def __init__(self, quantity, item_factory, collection_rate=1):
        self.quantity = quantity
        self.item_factory = item_factory
        self.exhausted = False
        self.collection_rate = collection_rate

    def collect(self, max_collection=None):
        #TODO find some sort of scailing collection rate
        if not self.exhausted:
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

    def remaining_ore(self):
        return self.quantity



class Container():
    pass

class Collidable():
    pass
