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


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2 or force:
            if self.dirty == 1:
                self.dirty = 0

            if self.collided and not self.selected:
                cpy = self.image.copy()
                cpy.fill(pygame.Color("#000000"), rect=(0, 0, 4, config.image_size[1]))
                cpy.fill(pygame.Color("#000000"), rect=(config.image_size[0] - 4, 0, 4, config.image_size[1]))
                cpy.fill(pygame.Color("#000000"), rect=(0, 0, config.image_size[1], 4))
                cpy.fill(pygame.Color("#000000"), rect=(0, config.image_size[0] - 4, config.image_size[1], 4))

                surf.blit(cpy, (self.rect.x, self.rect.y))

            elif self.selected and not self.collided:
                cpy = self.image.copy()
                cpy.fill(pygame.Color("#FFFFFF"), rect=(0, 0, 4, config.image_size[1]))
                cpy.fill(pygame.Color("#FFFFFF"), rect=(config.image_size[0] - 4, 0, 4, config.image_size[1]))
                cpy.fill(pygame.Color("#FFFFFF"), rect=(0, 0, config.image_size[1], 4))
                cpy.fill(pygame.Color("#FFFFFF"), rect=(0, config.image_size[0] - 4, config.image_size[1], 4))

                surf.blit(cpy, (self.rect.x, self.rect.y))

            elif self.selected and self.collided:
                cpy = self.image.copy()
                cpy.fill(pygame.Color("#AAAAAA"), rect=(0, 0, 4, config.image_size[1]))
                cpy.fill(pygame.Color("#AAAAAA"), rect=(config.image_size[0] - 4, 0, 4, config.image_size[1]))
                cpy.fill(pygame.Color("#AAAAAA"), rect=(0, 0, config.image_size[1], 4))
                cpy.fill(pygame.Color("#AAAAAA"), rect=(0, config.image_size[0] - 4, config.image_size[1], 4))

                surf.blit(cpy, (self.rect.x, self.rect.y))

            else:
                return surf.blit(self.image, (self.rect.x, self.rect.y))


class OreDeposit():
    def __init__(self, quantity):
        self.quantity = quantity

    def collect(self):
        #TODO find some sort of scailing collection rate
        self.quantity -= 10
        return 10

    def remaining_ore(self):
        return self.quantity

