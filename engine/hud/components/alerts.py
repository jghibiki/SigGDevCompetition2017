import datetime

import pygame
from pygame.sprite import DirtySprite

from engine.hud.components.component import ScreenComponent
from engine.utils import wrapline

class AlertComponent(ScreenComponent):

    def __init__(self, screen, viewport):
        w = 375
        h = 500
        x = 300
        y = 35
        ScreenComponent.__init__(self, screen, x, y, w, h, viewport)

        # TODO find better mechanism for sharing fonts
        self.font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)
        self.small_font = pygame.font.Font("assets/bitwise/bitwise.ttf", 15)

        self.surf = pygame.Surface((w, h), flags=pygame.SRCALPHA)
        self.num_alerts = 0

        self.last_update = datetime.datetime.now()

        self.updates = []


    def update(self):
        units = self.viewport.unit_layer

        changes = False

        avail_alerts = len(self.screen.state("alerts"))

        now = datetime.datetime.now()

        for alert in self.screen.state("alerts"):
            if alert["expiration"] <= now:
                self.screen.state("alerts").remove(alert)

        changes = avail_alerts != self.num_alerts
        self.num_alerts = avail_alerts


        if self.dirty != 2:
            if changes: self.dirty = 1
        return changes or self.dirty == 2

    def render(self):
        if self.dirty:

            self.surf.fill(pygame.Color(0,0,0,0))

            tmp = self.font.render("Alerts: ", True, pygame.Color("#00AD03"))
            self.surf.blit(tmp, (5, 5))

            if len(self.screen.state("alerts")) > 0:
                now = datetime.datetime.now()

                y_offset = 0

                for alert in self.screen.state("alerts"):
                    text = wrapline("<" + alert["message"] + ">", self.small_font, 700)
                    for line in text:
                        rendered_text = self.small_font.render(line, True, pygame.Color("#00AD03"))
                        self.surf.blit(rendered_text, (5, 45 + y_offset * 15))
                        y_offset += 1



    def draw(self, surf, force=False):
        if self.dirty == 1 or self.dirty == 2  or force:
            if self.dirty == 1: self.dirty = 0

            surf.blit(self.surf, self.rect.topleft)
            self.updates = []
