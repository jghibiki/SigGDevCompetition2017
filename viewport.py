import math

import pygame
from pygame.locals import *

import config
from block import *


class Viewport():

    def __init__(self, virtual_width, virtual_height, map_height, map_width):


        self.v_rect = pygame.Rect(0, 0, virtual_width, virtual_height-config.hud_size)
        self.map_rect = pygame.Rect(0, 0, map_width, map_height)
        self.hud_rect = pygame.Rect(0, virtual_height-config.hud_size, virtual_width, config.hud_size)

        self.map_layer = []
        self.map_layer_surf= pygame.Surface((self.map_rect.w, self.map_rect.h))

        self.item_layer = []
        self.item_layer_surf= pygame.Surface((self.map_rect.w, self.map_rect.h), flags=pygame.SRCALPHA)

        self.unit_layer = []
        self.unit_layer_surf= pygame.Surface((self.map_rect.w, self.map_rect.h))

        self.hud_surf = pygame.Surface((self.hud_rect.w, self.hud_rect.h))
        self.hud_surf.fill(pygame.Color("#737373"))


        self.dirty = 1

        self.font = pygame.font.Font(None, 20)

        self.mouse_events = []

    def south(self):
        if abs(self.v_rect.y) + 5 < self.map_rect.h - config.window_size[1] + config.hud_size:
            self.v_rect.y += 5
        elif abs(self.v_rect.y) + 1 < self.map_rect.h - config.window_size[1]:
            self.v_rect.y += 1

    def north(self):
        if  abs(self.v_rect.y) - 5 >= 0:
            self.v_rect.y -= 5
        elif abs(self.v_rect.y) - 1 >= 0:
            self.v_rect.y -= 1


    def east(self):
        if abs(self.v_rect.x) + 5 < self.map_rect.w - config.window_size[0]:
            self.v_rect.x += 5
        elif abs(self.v_rect.x) + 1 < self.map_rect.w - config.window_size[0]:
            self.v_rect.x += 1


    def west(self):
        if abs(self.v_rect.x) - 5 >= 0:
            self.v_rect.x -= 5
        elif abs(self.v_rect.x) - 1 >= 0:
            self.v_rect.x -= 1


    def handle_keyboard_events(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.north()

        if keys[K_DOWN]:
            self.south()

        if keys[K_LEFT]:
            self.west()

        if keys[K_RIGHT]:
            self.east()

    def handle_mouse_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for y in self.item_layer:
            for x in y:
                if x is not None:
                    if x.mouse_collide(mouse_pos):
                        for event in self.mouse_events:
                            if x.mouse_collide(event.pos, side_effect=False):
                                x.toggle_selected()
        self.mouse_events = []



    def render(self):
        if self.dirty == 1 or self.dirty == 2:
            if self.dirty == 1:
                self.dirty = 0

            diff_rects = []
            self.item_layer_surf.fill(pygame.Color(0, 0, 0, 1))
            for y in range(0, config.world_size[0]):
                for x in range(0, config.world_size[1]):
                    map_diff = self.map_layer[y][x].draw(self.map_layer_surf)

                    item_diff = None
                    if self.item_layer[y][x] != None:
                        item_diff = self.item_layer[y][x].draw(self.item_layer_surf, force=True)

                    diff_rects.extend([ map_diff, item_diff ])



    def draw(self, surf):
        rects = [ ]

        # draw map layer
        rects.append( surf.blit(self.map_layer_surf, (0, 0),  area=self.v_rect) )

        # item layer
        rects.append( surf.blit(self.item_layer_surf, (0, 0),  area=self.v_rect) )

        # draw hud layer
        rects.append( surf.blit(self.hud_surf, (self.hud_rect.x, self.hud_rect.y)) )


        return rects



