import math

import pygame
from pygame.sprite import DirtySprite

from engine import config
from engine.hud.components.component import ScreenComponent

class PauseComponent(ScreenComponent):
    def __init__(self, screen, viewport):

        # TODO find better mechanism for sharing fonts
        self.font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)
        self.text = "*Paused*"
        w, h = self.font.size(self.text)
        x = math.floor(config.window_size[0]/2) - math.floor(w/2)
        y = 5

        ScreenComponent.__init__(self, screen, x, y, w, h, viewport)

        self.paused = False
        self.paused_color = pygame.Color("#00AD03")
        self.unpaused_color = pygame.Color("#001700")

        self.dirty = 1


    def update(self):
        old = self.paused
        self.paused = self.screen.state("enterprise") is not None and self.screen.state("enterprise").paused

        if old != self.paused:
            self.dirty = 2 if self.dirty == 2 else 1
            return True
        return False

    def render(self):
        if self.dirty:

            if self.paused:
                paused_color = self.paused_color
            else:
                paused_color = self.unpaused_color

            self.surf = self.font.render(self.text, True, paused_color)


    def draw(self, surf, force=False):
        if self.dirty:
            if self.dirty != 2:
                self.dirty = 0
            surf.blit(self.surf, self.rect.topleft)
