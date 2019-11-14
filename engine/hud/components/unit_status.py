import pygame
from pygame.sprite import DirtySprite

from engine.hud.components.component import ScreenComponent
from engine.dispatch import *

class UnitStatusComponent(ScreenComponent):

    def __init__(self, screen, viewport):
        w = 290
        h = 500
        x = 10
        y = 45
        ScreenComponent.__init__(self, screen, x, y, w, h, viewport)

        # TODO find better mechanism for sharing fonts
        self.font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)

        self.surf = pygame.Surface((w, h), flags=pygame.SRCALPHA)

        self.updates = []

        self.screen.register_state("hovered_unit", None)
        self.screen.register_state("hovered_stock_pile", None)
        self.screen.register_state("hovered_building_placeholder", None)

        self.fully_functioning_units = 0
        self.malfunctioning_units = 0
        self.rogue_units = 0
        self.idle_units = 0
        self.num_tasks = 0

    def update(self):
        units = self.viewport.unit_layer

        changes = False

        old = self.fully_functioning_units
        self.fully_functioning_units = len(list(filter(lambda x: x.cooperation_rating >= 5, units)))
        changes = self.fully_functioning_units != old

        old = self.malfunctioning_units
        self.malfunctioning_units = len(list(filter(lambda x: 0 < x.cooperation_rating < 5, units)))
        changes = changes or self.malfunctioning_units != old

        old = self.rogue_units
        self.rogue_units = len(list(filter(lambda x: x.cooperation_rating <= 0, units)))
        changes = changes or self.rogue_units != old

        old = self.idle_units
        self.idle_units = len(list(filter(lambda x: x.task is None or isinstance(x.task, IdleTask), units)))
        changes = changes or self.idle_units != old

        old = self.num_tasks
        self.num_tasks = len(self.screen.state("dispatcher").tasks)
        changes = changes or self.num_tasks != old

        if self.dirty != 2:
            if changes: self.dirty = 1
        return changes or self.dirty == 2

    def render(self):
        if self.dirty:

            self.surf.fill(pygame.Color(0,0,0,0))

            tmp = self.font.render("Functioning Units: {0}".format(self.fully_functioning_units), True, pygame.Color("#00AD03"))
            diff = self.surf.blit(tmp, (0, 0))
            self.updates.append(diff)

            tmp = self.font.render("Malfunctioning Units: {0}".format(self.malfunctioning_units), True, pygame.Color("#00AD03"))
            diff = self.surf.blit(tmp, (0, 25))
            self.updates.append(diff)

            tmp = self.font.render("Rogue Units: {0}".format(self.rogue_units), True, pygame.Color("#00AD03"))
            diff = self.surf.blit(tmp, (0, 50))
            self.updates.append(diff)

            tmp = self.font.render("Idle Units: {0}".format(self.idle_units), True, pygame.Color("#00AD03"))
            diff = self.surf.blit(tmp, (0, 75))
            self.updates.append(diff)

            tmp = self.font.render("Availiable Tasks: {0}".format(self.num_tasks), True, pygame.Color("#00AD03"))
            diff = self.surf.blit(tmp, (0, 100))
            self.updates.append(diff)


    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2  or force:
            if self.dirty == 1: self.dirty = 0

            surf.blit(self.surf, self.rect.topleft)
            self.updates = []
