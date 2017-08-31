import pygame
from pygame.sprite import DirtySprite

class ScreenComponent(DirtySprite):
    def __init__(self, screen, x, y, w, h, viewport):
        DirtySprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.viewport = viewport
        self.dirty = 1


    def update(self):
        raise Exception("ScreenComponent.update not implemented in child")

    def render(self):
        raise Exception("ScreenComponent.render not implemented in child")

    def draw(self, surf, force=False):
        raise Exception("ScreenComponent.draw not implemented in child")

