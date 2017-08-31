import pygame
from pygame.sprite import DirtySprite


class Menu(DirtySprite):
    def __init__(self, viewport, x, y, w, h):
        DirtySprite.__init__(self)

        self.viewport = viewport

        self.rect = pygame.Rect(x, y, w, h)

    def update(self):
        pass

    def render(self):
        pass

    def draw(self, surf, force=False):
        pass

