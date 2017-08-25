import math
import datetime
from collections import Counter

import pygame
from pygame.sprite import DirtySprite

import config
from utils import wrapline
from dispatch import *

class Hud(DirtySprite):

    def __init__(self,x, y, w, h, viewport):
        DirtySprite.__init__(self)

        self.viewport = viewport
        self.enterprise = None
        self.dispatcher = None

        self.rect = pygame.Rect(x, y, w, h)

        self.font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)
        self.small_font = pygame.font.Font("assets/bitwise/bitwise.ttf", 15)

        self.hovered_unit = None
        self.hovered_stock_pile = None
        self.hovered_building_placeholder = None

        self.dirty = 2

        self.alerts = []


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty ==2  or force:
            if self.dirty == 1: self.dirty = 0

            units = self.viewport.unit_layer

            # clear hud
            surf.fill(pygame.Color("#000000"))

            pygame.draw.line(surf, pygame.Color("#00AD03"),
                    (10, 35),
                    (config.window_size[0]-10, 35))


            fully_functioning_units = len(list(filter(lambda x: x.cooperation_rating >= 5, units)))
            unit_count = self.font.render("Functioning Units: {0}".format(fully_functioning_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (10, 45))

            malfunctioning_units = len(list(filter(lambda x: 0 < x.cooperation_rating < 5, units)))
            unit_count = self.font.render("Malfunctioning Units: {0}".format(malfunctioning_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (10, 70))

            rogue_units = len(list(filter(lambda x: x.cooperation_rating <= 0, units)))
            unit_count = self.font.render("Rogue Units: {0}".format(rogue_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (10, 95))

            idle_units = len(list(filter(lambda x: x.task is None or isinstance(x.task, IdleTask), units)))
            unit_count = self.font.render("Idle Units: {0}".format(idle_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (10, 120))

            num_tasks = len(self.dispatcher.tasks)
            num_tasks = self.font.render("Availiable Tasks: {0}".format(num_tasks), True, pygame.Color("#00AD03"))
            surf.blit(num_tasks, (10, 145))

            # alert rendering
            pygame.draw.line(surf, pygame.Color("#00AD03"), (300, 35), (300, config.hud_size - 5))

            pygame.draw.line(surf, pygame.Color("#00AD03"), (675, 35), (675, config.hud_size - 5))

            unit_count = self.font.render("Alerts: ", True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (305, 35))

            if len(self.alerts) > 0:
                y_offset = 1
                now = datetime.datetime.now()

                for alert in self.alerts:
                    if alert["expiration"] > now:
                        text = wrapline("<" + alert["message"] + ">", self.small_font, 700)
                        for line in text:
                            rendered_text = self.small_font.render(line, True, pygame.Color("#00AD03"))
                            surf.blit(rendered_text, (305, 45 + y_offset * 15))
                            y_offset += 1
                    else:
                        self.alerts.remove(alert)


            # render unit info on hover
            if self.hovered_unit:
                unit_name = self.font.render(self.hovered_unit.name, True, pygame.Color("#00AD03"))
                surf.blit(unit_name, (700, 35))

                height_offset = 60
                height_offset_inc = 15

                if self.hovered_unit.task is not None:
                    unit_name = self.small_font.render("Task: " + self.hovered_unit.task.description, True, pygame.Color("#00AD03"))
                    surf.blit(unit_name, (700, height_offset))
                    height_offset += height_offset_inc
                else:
                    unit_name = self.small_font.render("Task: None", True, pygame.Color("#00AD03"))
                    surf.blit(unit_name, (700, height_offset))
                    height_offset += height_offset_inc

                unit_name = self.small_font.render(
                        "Inventory: {0}/{1}".format(
                            len(self.hovered_unit.inventory),
                            self.hovered_unit.inventory_size),
                        True, pygame.Color("#00AD03"))
                surf.blit(unit_name, (700, height_offset))
                height_offset += height_offset_inc

                simple_inv = [ item.name for item in self.hovered_unit.inventory ]
                unique = set(simple_inv)
                counter = Counter(simple_inv)

                y_offset = 0

                for item in unique:
                    unit_name = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                    surf.blit(unit_name, (700, height_offset + y_offset * height_offset_inc))
                    y_offset += 1


            elif self.hovered_stock_pile:
                stock_pile = self.font.render("Stockpile", True, pygame.Color("#00AD03"))
                surf.blit(stock_pile, (700, 35))

                contents = self.small_font.render(
                        "Contents: {0}/{1}".format(
                            len(self.hovered_stock_pile.items),
                            self.hovered_stock_pile.capacity),
                        True, pygame.Color("#00AD03"))
                surf.blit(contents, (700, 60))

                simple_contents = [ item.name for item in self.hovered_stock_pile.items ]
                unique = set(simple_contents)
                counter = Counter(simple_contents)

                y_offset = 0

                for item in unique:
                    contents = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                    surf.blit(contents, (700, 85 + y_offset * 15))
                    y_offset += 1

            elif self.hovered_building_placeholder:
                placeholder_title = self.font.render("Building {}...".format(self.hovered_building_placeholder.type_factory.name), True, pygame.Color("#00AD03"))
                surf.blit(placeholder_title, (700, 35))

                # calculate competion
                count = sum([ e["collected"] for e in self.hovered_building_placeholder.requirements])
                needed = sum([ e["needed"] for e in self.hovered_building_placeholder.requirements])
                percent_complete = (count/needed)*100

                needed_materials = [ e["type"].name for e in self.hovered_building_placeholder.requirements if e["needed"] > e["collected"] ]
                needed_materials_text = ', '.join(needed_materials)

                content1 = self.small_font.render(
                        "{}% Complete".format(percent_complete), True, pygame.Color("#00AD03"))
                surf.blit(content1, (700, 60))

                content2 = self.small_font.render(
                        "Needs: {}".format(needed_materials_text), True, pygame.Color("#00AD03"))
                surf.blit(content2, (700, 85))



            else: # render stats

                if self.enterprise is not None:
                    month_day = self.font.render("Month {0}, Day {1} ".format(
                        self.enterprise.current_month,
                        self.enterprise.current_day),
                        True, pygame.Color("#00AD03"))
                    surf.blit(month_day, (700, 35))

                    profit = self.font.render("Export Quota: ${0}/${1}".format(
                        self.enterprise.funds,
                        self.enterprise.monthly_quota),
                        True, pygame.Color("#00AD03"))
                    surf.blit(profit, (700, 60))

                    render = self.small_font.render("Availiable Resources:".format(
                        self.enterprise.funds,
                        self.enterprise.monthly_quota),
                        True, pygame.Color("#00AD03"))
                    surf.blit(render, (700, 85))

                    items = []
                    for stock_pile in self.dispatcher.stock_piles:
                        items.extend( [ item.name for item in stock_pile.items ] )

                    unique = set(items)
                    counter = Counter(items)

                    y_offset = 0

                    for item in unique:
                        contents = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                        surf.blit(contents, (700, 110 + y_offset * 12))
                        y_offset += 1


            if self.enterprise is not None and self.enterprise.paused:
                paused_color = pygame.Color("#00AD03")

            else:
                paused_color = pygame.Color("#001700")

            paused = self.font.render("*Paused*", True, paused_color)
            surf.blit(paused, (
                math.floor(config.window_size[0]/2) - math.floor(paused.get_rect().w/2),
                5))

            pygame.draw.line(surf, pygame.Color("#00AD03"),
                    (math.floor(config.window_size[0]/2) - 75, 5),
                    (math.floor(config.window_size[0]/2) - 75, 35))

            pygame.draw.line(surf, pygame.Color("#00AD03"),
                (math.floor(config.window_size[0]/2) + 75, 5),
                (math.floor(config.window_size[0]/2) + 75, 35))




    def add_alert(self, msg):
        if len(self.alerts) == 4: # remove alert before adding another
            to_remove = min(self.alerts, key=lambda x: x["expiration"])
            self.alerts.remove(to_remove)

        self.alerts.append({
            "expiration": datetime.datetime.now() + datetime.timedelta(seconds=5),
            "message": msg})


