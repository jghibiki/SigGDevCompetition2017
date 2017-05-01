import math

import pygame
from pygame.locals import *

import config
from hud import Hud
from block import *
from items import *


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
        self.unit_layer_surf= pygame.Surface((self.map_rect.w, self.map_rect.h), flags=pygame.SRCALPHA)

        self.unit_action_surf = pygame.Surface((self.map_rect.w, self.map_rect.h), flags=pygame.SRCALPHA)

        self.hud = Hud(0, virtual_height-config.hud_size, virtual_width, config.hud_size, self)
        self.hud_surf = pygame.Surface((self.hud_rect.w, self.hud_rect.h))
        self.hud_surf.fill(pygame.Color("#737373"))
        self.hud_font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)

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
                    if isinstance(x, list):
                        for item in x:
                            if item.mouse_collide(mouse_pos):
                                for event in self.mouse_events:
                                    if item.mouse_collide(event.pos, side_effect=False):
                                        item.toggle_selected()
                    else:
                        if x.mouse_collide(mouse_pos):
                            for event in self.mouse_events:
                                if x.mouse_collide(event.pos, side_effect=False):
                                    x.toggle_selected()

        hovering_unit = False
        for unit in self.unit_layer:
            if unit.mouse_collide():
                self.hud.hovered_unit = unit
                self.dirty = 1
                hovering_unit = True
                break

        if not hovering_unit and self.hud.hovered_unit != None:
            self.hud.hovered_unit = None
            self.dirty = 1

        hovering_stock_pile = False
        for y in self.item_layer:
            for x in y:
                if isinstance(x, Stockpile):
                    if x.mouse_collide(mouse_pos, side_effect=False) or x.mouse_collide(side_effect=False):
                        self.hud.hovered_stock_pile= x
                        self.dirty = 1
                        hovering_stock_pile= True
                        break

        if not hovering_stock_pile and self.hud.hovered_stock_pile != None:
            self.hud.hovered_stock_pile = None
            self.dirty = 1

        self.mouse_events = []

    def render(self):
        if self.dirty == 1 or self.dirty == 2:
            if self.dirty == 1:
                self.dirty = 0

            diff_rects = []
            for y in range(0, config.world_size[0]):
                for x in range(0, config.world_size[1]):
                    map_diff = self.map_layer[y][x].draw(self.map_layer_surf)

                    item_diff = None
                    if self.item_layer[y][x] != None:
                        if isinstance(self.item_layer[y][x], list):
                            for item in self.item_layer[y][x]:
                                item_diff = item.draw(self.item_layer_surf)
                            diff_rects.append(item_diff)
                        else: # not a list
                            item_diff = self.item_layer[y][x].draw(self.item_layer_surf)
                            diff_rects.append(item_diff)

                    diff_rects.append(map_diff)

            for unit in self.unit_layer:
                unit.draw(self.unit_layer_surf)

            self.unit_action_surf.fill(pygame.Color(0, 0, 0, 1))
            for unit in self.unit_layer:
                unit.draw_action(self.unit_action_surf)

            self.hud.draw(self.hud_surf)




    def draw(self, surf):
        rects = [ ]

        # draw map layer
        rects.append( surf.blit(self.map_layer_surf, (0, 0),  area=self.v_rect) )

        # item layer
        rects.append( surf.blit(self.item_layer_surf, (0, 0),  area=self.v_rect) )

        # unit layer
        rects.append( surf.blit(self.unit_layer_surf, (0, 0),  area=self.v_rect) )

        # unit action layer
        rects.append( surf.blit(self.unit_action_surf, (0, 0),  area=self.v_rect) )

        # draw hud layer
        rects.append( surf.blit(self.hud_surf, (self.hud_rect.x, self.hud_rect.y)) )


        return rects



