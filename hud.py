import datetime
from collections import Counter

import pygame
from pygame.sprite import DirtySprite

import config
from utils import wrapline

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

        self.dirty = 2

        self.alerts = []


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty ==2  or force:
            if self.dirty == 1: self.dirty = 0

            units = self.viewport.unit_layer

            # clear hud
            surf.fill(pygame.Color("#000000"))

            fully_functioning_units = len(list(filter(lambda x: x.cooperation_rating >= 5, units)))
            unit_count = self.font.render("Functioning Units: {0}".format(fully_functioning_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (10, 10))

            malfunctioning_units = len(list(filter(lambda x: 0 < x.cooperation_rating < 5, units)))
            unit_count = self.font.render("Malfunctioning Units: {0}".format(malfunctioning_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (10, 35))

            rogue_units = len(list(filter(lambda x: x.cooperation_rating <= 0, units)))
            unit_count = self.font.render("Rogue Units: {0}".format(rogue_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (10, 60))

            idle_units = len(list(filter(lambda x: not x.task, units)))
            unit_count = self.font.render("Idle Units: {0}".format(rogue_units), True, pygame.Color("#00AD03"))
            surf.blit(unit_count, (300, 10))

            # alert rendering
            pygame.draw.line(surf, pygame.Color("#00AD03"), (445, 5), (445, config.hud_size - 5))

            pygame.draw.line(surf, pygame.Color("#00AD03"), (675, 5), (675, config.hud_size - 5))

            if True or len(self.alerts) > 0: #TODO remove true
                unit_count = self.font.render("Alerts: ", True, pygame.Color("#00AD03"))
                surf.blit(unit_count, (455, 10))

                y_offset = 1
                now = datetime.datetime.now()

                for alert in self.alerts:
                    if alert["expiration"] > now:
                        text = wrapline("<" + alert["message"] + ">", self.small_font, 500)
                        for line in text:
                            rendered_text = self.small_font.render(line, True, pygame.Color("#00AD03"))
                            surf.blit(rendered_text, (445, 20 + y_offset * 15))
                            y_offset += 1
                    else:
                        self.alerts.remove(alert)


            # render unit info on hover
            if self.hovered_unit:
                unit_name = self.font.render(self.hovered_unit.name, True, pygame.Color("#00AD03"))
                surf.blit(unit_name, (700, 10))

                unit_name = self.small_font.render(
                        "Inventory: {0}/{1}".format(
                            len(self.hovered_unit.inventory),
                            self.hovered_unit.inventory_size),
                        True, pygame.Color("#00AD03"))
                surf.blit(unit_name, (700, 35))

                simple_inv = [ item.name for item in self.hovered_unit.inventory ]
                unique = set(simple_inv)
                counter = Counter(simple_inv)

                y_offset = 0

                for item in unique:
                    unit_name = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                    surf.blit(unit_name, (700, 50 + y_offset * 15))
                    y_offset += 1


            elif self.hovered_stock_pile:
                stock_pile = self.font.render("Stockpile", True, pygame.Color("#00AD03"))
                surf.blit(stock_pile, (700, 10))

                contents = self.small_font.render(
                        "Contents: {0}/{1}".format(
                            len(self.hovered_stock_pile.items),
                            self.hovered_stock_pile.capacity),
                        True, pygame.Color("#00AD03"))
                surf.blit(contents, (700, 35))

                simple_contents = [ item.name for item in self.hovered_stock_pile.items ]
                unique = set(simple_contents)
                counter = Counter(simple_contents)

                y_offset = 0

                for item in unique:
                    contents = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                    surf.blit(contents, (700, 50 + y_offset * 15))
                    y_offset += 1

            else: # render stats

                if self.enterprise is not None:
                    month_day = self.font.render("Month {0}, Day {1} ".format(
                        self.enterprise.current_month,
                        self.enterprise.current_day),
                        True, pygame.Color("#00AD03"))
                    surf.blit(month_day, (700, 10))

                    profit = self.font.render("Export Quota: ${0}/${1}".format(
                        self.enterprise.funds,
                        self.enterprise.monthly_quota),
                        True, pygame.Color("#00AD03"))
                    surf.blit(profit, (700, 35))

                    render = self.small_font.render("Availiable Resources:".format(
                        self.enterprise.funds,
                        self.enterprise.monthly_quota),
                        True, pygame.Color("#00AD03"))
                    surf.blit(render, (700, 60))

                    items = []
                    for stock_pile in self.dispatcher.stock_piles:
                        items.extend( [ item.name for item in stock_pile.items ] )

                    unique = set(items)
                    counter = Counter(items)

                    y_offset = 0

                    for item in unique:
                        contents = self.small_font.render("- {0}x{1}".format(counter[item], item), True, pygame.Color("#00AD03"))
                        surf.blit(contents, (700, 75 + y_offset * 12))
                        y_offset += 1




    def add_alert(self, msg):
        if len(self.alerts) == 2: # remove alert before adding another
            to_remove = min(self.alerts, key=lambda x: x["expiration"])
            self.alerts.remove(to_remove)

        self.alerts.append({
            "expiration": datetime.datetime.now() + datetime.timedelta(seconds=15),
            "message": msg})


