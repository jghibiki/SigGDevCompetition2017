
import pygame, sys, random, math
import pygame.gfxdraw
from pygame.locals import *
from pygame.sprite import LayeredDirty

import config
from block import *
from viewport import Viewport
from generator import *

pygame.init()
clock = pygame.time.Clock()

info = pygame.display.Info()

config.window_size = (math.floor(info.current_w * config.display_scale), math.floor(info.current_h * config.display_scale))

bestdepth = pygame.display.mode_ok(config.window_size)
window_surf = pygame.display.set_mode(config.window_size, 0, bestdepth) #, pygame.FULLSCREEN);

pygame.display.set_caption("Some Mining Game");

pygame.font.init()

init_block_images()

vp = Viewport(
    config.window_size[0],
    config.window_size[1],
    config.world_size[0] * config.image_size[0],
    config.world_size[1] * config.image_size[1]
)


# generate map layer
for y in range(0, config.world_size[1]):
    col = []
    for x in range(0, config.world_size[0]):
        col.append( Grass(x, y) )
    vp.map_layer.append(col)

for y in range(0, config.world_size[1]):
    col = []
    for x in range(0, config.world_size[0]):
        col.append( None )
    vp.item_layer.append(col)

# generate item layer
generate_items_layer(vp)


counter = 0

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == MOUSEBUTTONUP:
            vp.mouse_events.append(event)

    if counter % 40 == 1:
        counter = 0

        vp.handle_keyboard_events()
        vp.handle_mouse_events()


    vp.render()

    rects = vp.draw(window_surf)

    counter += 1
    pygame.display.update(rects)
    clock.tick(120)


