import math
from collections import Counter

import pygame
from pygame.sprite import DirtySprite

from engine import config
from engine.hud.menu import Menu
from engine.hud.parent import ParentScreen
from engine.hud.child import ChildScreen
from engine.hud.components import *

class MainHudScreen(Menu, ParentScreen, ChildScreen):
    def __init__(self, parent, x, y, w, h, viewport):
        Menu.__init__(self, viewport, x, y, w, h)
        ParentScreen.__init__(self)
        ChildScreen.__init__(self, parent)

        self.rect = pygame.Rect(x, y, w, h)
        self.surf = pygame.Surface((w, h), flags=pygame.SRCALPHA)

        self.font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)
        self.small_font = pygame.font.Font("assets/bitwise/bitwise.ttf", 15)


        self.children = [
            UnitStatusComponent(self, viewport),
            PauseComponent(self, viewport),
            AlertComponent(self, viewport)
        ]

        self.updates = []

        self.dirty = 1

    def update(self):
        for child in self.children:
            if child.update():
                self.dirty = 1

        if self.dirty:
            return True
        return False

    def render(self):
        if self.dirty == 1 or self.dirty == 2:
            for child in self.children:
                if child.dirty:
                    child.render()
                    self.updates.append(child.rect.inflate(1, 1))


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty ==2  or force:
            if self.dirty == 1: self.dirty = 0

            units = self.viewport.unit_layer

            # clear hud
            for r in  self.updates:
                self.surf.fill(pygame.Color(0,0,0,0), rect=r)
            self.updates = []

            pygame.draw.line(self.surf, pygame.Color("#00AD03"),
                    (10, 35),
                    (config.window_size[0]-10, 35))

            for child in self.children:
                child.draw(self.surf, force)


            # alert rendering
            pygame.draw.line(self.surf, pygame.Color("#00AD03"), (300, 35), (300, config.hud_size - 5))

            pygame.draw.line(self.surf, pygame.Color("#00AD03"), (675, 35), (675, config.hud_size - 5))



            # render unit info on hover
            if self.parent.state("hovered_unit"):
                unit_name = self.font.render(self.parent.state("hovered_unit").name, True, pygame.Color("#00AD03"))
                surf.blit(unit_name, (700, 35))

                height_offset = 60
                height_offset_inc = 15

                if self.parent.state("hovered_unit").task is not None:
                    unit_name = self.small_font.render("Task: " + self.parent.state("hovered_unit").task.description, True, pygame.Color("#00AD03"))
                    surf.blit(unit_name, (700, height_offset))
                    height_offset += height_offset_inc
                else:
                    unit_name = self.small_font.render("Task: Seeking task.", True, pygame.Color("#00AD03"))
                    surf.blit(unit_name, (700, height_offset))
                    height_offset += height_offset_inc

                unit_name = self.small_font.render(
                        "Inventory: {0}/{1}".format(
                            len(self.parent.state("hovered_unit").inventory),
                            self.parent.state("hovered_unit").inventory_size),
                        True, pygame.Color("#00AD03"))
                surf.blit(unit_name, (700, height_offset))
                height_offset += height_offset_inc

                simple_inv = [ item.name for item in self.parent.state("hovered_unit").inventory ]
                unique = set(simple_inv)
                counter = Counter(simple_inv)

                y_offset = 0

                for item in unique:
                    unit_name = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                    surf.blit(unit_name, (700, height_offset + y_offset * height_offset_inc))
                    y_offset += 1


            elif self.parent.state("hovered_stock_pile"):
                stock_pile = self.font.render("Stockpile", True, pygame.Color("#00AD03"))
                surf.blit(stock_pile, (700, 35))

                contents = self.small_font.render(
                        "Contents: {0}/{1}".format(
                            len(self.parent.state("hovered_stock_pile").items),
                            self.parent.state("hovered_stock_pile").capacity),
                        True, pygame.Color("#00AD03"))
                surf.blit(contents, (700, 60))

                simple_contents = [ item.name for item in self.parent.state("hovered_stock_pile").items ]
                unique = set(simple_contents)
                counter = Counter(simple_contents)

                y_offset = 0

                for item in unique:
                    contents = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                    surf.blit(contents, (700, 85 + y_offset * 15))
                    y_offset += 1

            elif self.parent.state("hovered_building_placeholder"):
                placeholder_title = self.font.render("Building {}...".format(self.parent.state("hovered_building_placeholder").type_factory.name), True, pygame.Color("#00AD03"))
                surf.blit(placeholder_title, (700, 35))

                # calculate competion
                count = sum([ e["collected"] for e in self.parent.state("hovered_building_placeholder").requirements])
                needed = sum([ e["needed"] for e in self.parent.state("hovered_building_placeholder").requirements])
                percent_complete = (count/needed)*100

                needed_materials = [ e["type"].name for e in self.parent.state("hovered_building_placeholder").requirements if e["needed"] > e["collected"] ]
                needed_materials_text = ', '.join(needed_materials)

                content1 = self.small_font.render(
                        "{}% Complete".format(percent_complete), True, pygame.Color("#00AD03"))
                surf.blit(content1, (700, 60))

                content2 = self.small_font.render(
                        "Needs: {}".format(needed_materials_text), True, pygame.Color("#00AD03"))
                surf.blit(content2, (700, 85))



            else: # render stats

                if self.parent.state("enterprise") is not None:
                    month_day = self.font.render("Month {0}, Day {1} ".format(
                        self.parent.state("enterprise").current_month,
                        self.parent.state("enterprise").current_day),
                        True, pygame.Color("#00AD03"))
                    surf.blit(month_day, (700, 35))

                    profit = self.font.render("Export Quota: ${0}/${1}".format(
                        self.parent.state("enterprise").funds,
                        self.parent.state("enterprise").monthly_quota),
                        True, pygame.Color("#00AD03"))
                    surf.blit(profit, (700, 60))

                    render = self.small_font.render("Availiable Resources:".format(
                        self.parent.state("enterprise").funds,
                        self.parent.state("enterprise").monthly_quota),
                        True, pygame.Color("#00AD03"))
                    surf.blit(render, (700, 85))

                    items = []
                    for stock_pile in self.parent.state("dispatcher").stock_piles:
                        items.extend( [ item.name for item in stock_pile.items ] )

                    unique = set(items)
                    counter = Counter(items)

                    y_offset = 0

                    for item in unique:
                        contents = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                        surf.blit(contents, (700, 110 + y_offset * 12))
                        y_offset += 1



            pygame.draw.line(surf, pygame.Color("#00AD03"),
                    (math.floor(config.window_size[0]/2) - 75, 5),
                    (math.floor(config.window_size[0]/2) - 75, 35))

            pygame.draw.line(surf, pygame.Color("#00AD03"),
                (math.floor(config.window_size[0]/2) + 75, 5),
                (math.floor(config.window_size[0]/2) + 75, 35))

        surf.blit(self.surf, (0, 0))

