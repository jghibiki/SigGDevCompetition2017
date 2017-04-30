
import pygame, sys, random, math
import pygame.gfxdraw
from pygame.locals import *
from pygame.sprite import LayeredDirty

import config
from block import *
from viewport import Viewport
from unit import Unit
from dispatch import Dispatcher, Task, GenericTarget
from generator import *
from utils import wrapline

pygame.init()
clock = pygame.time.Clock()

info = pygame.display.Info()

config.window_size = (math.floor(info.current_w * config.display_scale), math.floor(info.current_h * config.display_scale))

bestdepth = pygame.display.mode_ok(config.window_size)
window_surf = pygame.display.set_mode(config.window_size, 0, bestdepth) #, pygame.FULLSCREEN);

pygame.display.set_caption("Some Mining Game");

pygame.font.init()

title_font = pygame.font.Font("assets/bitwise/bitwise.ttf", 50)
title = title_font.render("Some Cyberpunk Mining Game", True, pygame.Color("#00AD03"))

loading_font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)
loading = title_font.render("Loading...", True, pygame.Color("#00AD03"))

window_surf.blit(title, (200, 100))
window_surf.blit(loading, (450, 300))
pygame.display.update()

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

#generate units
dispatcher = Dispatcher(vp)
#dispatcher.tasks.append( Task( GenericTarget( 20, 20) ) )
#dispatcher.tasks.append( Task( GenericTarget( 0, 20) ) )
#dispatcher.tasks.append( Task( GenericTarget( 20, 0) ) )
#dispatcher.tasks.append( Task( GenericTarget( 15, 7) ) )
#dispatcher.tasks.append( Task( GenericTarget( 50, 50) ) )
Unit.load_images()
num_units = 5

unit_count = 0
for y in range(0, config.world_size[1]):
    for x in range(0, config.world_size[0]):
        if vp.item_layer[y][x] == None:
            unit = Unit(x, y, vp, dispatcher)
            vp.unit_layer.append( unit )
            dispatcher.units.append( unit )
            unit_count += 1
            if unit_count >= num_units:
                break
    else:
        continue
    break


# do initial render while we are still on loading screen
vp.render()

#TODO: INSERT STORY HERE

story = "Welcome back to life.\n You died.\n Because of your outstanding debits, your body was claimed by DigiCorp Industries. In order to pay back your debit, You have been reanimated to serve as a laborer in our company. You will be unique among your co-workers. You have been allowed access to higher order brain functions in order to serve as a manager. It is your duty to build enough product to pay back your debit by commanding your assigned underlings. Once your debit is paid - including the costs of reanimation, you will be released. If you fail to complete your task our scientists will wipe your memory and your body will be repurposed as a manual laborer. Do not fail if you desire your freedom."


story_font = pygame.font.Font("assets/bitwise/bitwise.ttf", 25)

window_surf.fill(pygame.Color("#000000"))
y = 100
for split in story.split("\n"):
    for line in wrapline(split, story_font, config.window_size[0]):
            text = story_font.render(line, True, pygame.Color("#00AD03"))
            window_surf.blit(text,
                    (math.floor(
                        ( config.window_size[0]/2 ) - (text.get_rect().w/2) ),
                        y ))
            y += 25

loading = title_font.render("Press the Spacebar to continue...", True, pygame.Color("#00AD03"))

window_surf.blit(loading, (250, math.floor(config.window_size[1]*0.75)))
pygame.display.update()

cont = False
while not cont:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_SPACE:
                cont = True


# render once quick before first loop
window_surf.fill(pygame.Color("#000000"))
rects = vp.draw(window_surf)
pygame.display.update(rects)


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

    vp.handle_keyboard_events()
    vp.handle_mouse_events()

    if counter % 100 == 0:
        dispatcher.update()

    if counter == 1000:
        counter = 0

    vp.render()

    rects = vp.draw(window_surf)

    counter += 1
    pygame.display.update(rects)
    clock.tick(120)


