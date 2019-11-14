import math
import datetime

import pygame
from pygame.sprite import DirtySprite

import engine.config
from engine.utils import wrapline

from engine.hud.main_screen import MainHudScreen

class Hud(DirtySprite):

    def __init__(self, x, y, w, h, viewport):
        DirtySprite.__init__(self)

        self.rect = pygame.Rect(x, y, w, h)

        self.hud_state = {}
        self.children = [ MainHudScreen(self, x, y, w, h, viewport) ]

        self.surf = pygame.Surface((w, h), flags=pygame.SRCALPHA)
        self.surf.fill(pygame.Color("#000000"))

        self.register_state("alerts", [])

        self.updates = []

        self.dirty = 1


    def register_state(self, name, value):
        if name not in self.hud_state:
            self.hud_state[name] = value

    def state(self, name):
        if name in self.hud_state:
            return self.hud_state[name]
        return None

    def set_state(self, name, value):
        self.hud_state[name] = value


    def update(self):
        for c in self.children:
            if c.update():
                self.updates.append(c.rect)
                self.dirty = 1

    def render(self):
        for c in self.children:
            c.render()

    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty ==2  or force:
            if self.dirty == 1: self.dirty = 0

            for r in self.updates:
                self.surf.fill(pygame.Color("#000000"), r)
            self.updates = []

            for c in self.children:
                c.draw(self.surf, force)

            surf.blit(self.surf, (0, 0))


    def add_alert(self, msg):
        if len(self.state("alerts")) == 4: # remove alert before adding another
            to_remove = min(self.state("alerts"), key=lambda x: x["expiration"])
            self.state("alerts").remove(to_remove)

        self.state("alerts").append({
            "expiration": datetime.datetime.now() + datetime.timedelta(seconds=5),
            "message": msg})
