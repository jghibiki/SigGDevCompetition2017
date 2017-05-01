import random

from items import *

def generate_items_layer(vp):
    # generate item layer
    for s in range(0, 10):
        for y in range(0, config.world_size[1]):
            for x in range(0, config.world_size[0]):
                if not vp.item_layer[y][x]:
                    generate_stone_deposits(vp, x, y, s)

                if not vp.item_layer[y][x]:
                    generate_coal_deposits(vp, x, y, s)

                if not vp.item_layer[y][x]:
                    generate_copper_deposits(vp, x, y, s)

                if not vp.item_layer[y][x]:
                    generate_iron_deposits(vp, x, y, s)

                if not vp.item_layer[y][x]:
                    generate_trees(vp, x, y, s)

def generate_iron_deposits(vp, x, y, s):
    prob = 0.00125
    solo = True

    # above
    if y - 1 >= 0 and type(vp.item_layer[y-1][x])  == IronOreDeposit:
        prob += 0.05
        solo = False

    # below
    if y + 1 < config.world_size[1] and type(vp.item_layer[y+1][x])  == IronOreDeposit:
        prob += 0.05
        solo = False

    # left
    if x - 1 >= 0 and type(vp.item_layer[y][x-1])  == CopperOreDeposit:
        prob += 0.05
        solo = False

    # right
    if x + 1< config.world_size[0] and type(vp.item_layer[y][x+1])  == IronOreDeposit:
        prob += 0.05
        solo = False

    # above right
    if y - 1 >= 0 and x + 1 < config.world_size[0] and type(vp.item_layer[y][x+1]) == IronOreDeposit:
        prob += 0.05
        solo = False

    # above left
    if y - 1 >= 0 and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == IronOreDeposit:
        prob += 0.05
        solo = False

    # below left
    if y + 1 < config.world_size[1] and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == IronOreDeposit:
        prob += 0.05
        solo = False

    # below right
    if y + 1 < config.world_size[1] and x + 1 < config.world_size[1] and type(vp.item_layer[y][x+1]) == IronOreDeposit:
        prob += 0.05
        solo = False

    if solo:
        prob -=  0.0001 * s

    if prob > random.random():
        vp.item_layer[y][x] = IronOreDeposit(x, y, vp, random.randint(50, 150))


def generate_copper_deposits(vp, x, y, s):
    prob = 0.00125
    solo = True

    # above
    if y - 1 >= 0 and type(vp.item_layer[y-1][x])  == CopperOreDeposit:
        prob += 0.05
        solo = False

    # below
    if y + 1 < config.world_size[1] and type(vp.item_layer[y+1][x])  == CopperOreDeposit:
        prob += 0.05
        solo = False

    # left
    if x - 1 >= 0 and type(vp.item_layer[y][x-1])  == CopperOreDeposit:
        prob += 0.05
        solo = False

    # right
    if x + 1< config.world_size[0] and type(vp.item_layer[y][x+1])  == CopperOreDeposit:
        prob += 0.05
        solo = False

    # above right
    if y - 1 >= 0 and x + 1 < config.world_size[0] and type(vp.item_layer[y][x+1]) == CopperOreDeposit:
        prob += 0.05
        solo = False

    # above left
    if y - 1 >= 0 and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == CopperOreDeposit:
        prob += 0.05
        solo = False

    # below left
    if y + 1 < config.world_size[1] and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == CopperOreDeposit:
        prob += 0.05
        solo = False

    # below right
    if y + 1 < config.world_size[1] and x + 1 < config.world_size[1] and type(vp.item_layer[y][x+1]) == CopperOreDeposit:
        prob += 0.05
        solo = False

    if solo:
        prob -=  0.0001 * s

    if prob > random.random():
        vp.item_layer[y][x] = CopperOreDeposit(x, y, vp, random.randint(50, 150))


def generate_coal_deposits(vp, x, y, s):
    prob = 0.00125
    solo = True

    # above
    if y - 1 >= 0 and type(vp.item_layer[y-1][x])  == CoalDeposit:
        prob += 0.05
        solo = False

    # below
    if y + 1 < config.world_size[1] and type(vp.item_layer[y+1][x])  == CoalDeposit:
        prob += 0.05
        solo = False

    # left
    if x - 1 >= 0 and type(vp.item_layer[y][x-1])  == CoalDeposit:
        prob += 0.05
        solo = False

    # right
    if x + 1< config.world_size[0] and type(vp.item_layer[y][x+1])  == CoalDeposit:
        prob += 0.05
        solo = False

    # above right
    if y - 1 >= 0 and x + 1 < config.world_size[0] and type(vp.item_layer[y][x+1]) == CoalDeposit:
        prob += 0.05
        solo = False

    # above left
    if y - 1 >= 0 and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == CoalDeposit:
        prob += 0.05
        solo = False

    # below left
    if y + 1 < config.world_size[1] and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == CoalDeposit:
        prob += 0.05
        solo = False

    # below right
    if y + 1 < config.world_size[1] and x + 1 < config.world_size[1] and type(vp.item_layer[y][x+1]) == CoalDeposit:
        prob += 0.05
        solo = False

    if solo:
        prob -=  0.0001 * s

    if prob > random.random():
        vp.item_layer[y][x] = CoalDeposit(x, y, vp, random.randint(50, 150))

def generate_stone_deposits(vp, x, y, s):
    prob = 0.00125
    solo = True

    # above
    if y - 1 >= 0 and type(vp.item_layer[y-1][x])  == StoneDeposit:
        prob += 0.05
        solo = False

    # below
    if y + 1 < config.world_size[1] and type(vp.item_layer[y+1][x])  == StoneDeposit:
        prob += 0.05
        solo = False

    # left
    if x - 1 >= 0 and type(vp.item_layer[y][x-1])  == StoneDeposit:
        prob += 0.05
        solo = False

    # right
    if x + 1< config.world_size[0] and type(vp.item_layer[y][x+1])  == StoneDeposit:
        prob += 0.05
        solo = False

    # above right
    if y - 1 >= 0 and x + 1 < config.world_size[0] and type(vp.item_layer[y][x+1]) == StoneDeposit:
        prob += 0.05
        solo = False

    # above left
    if y - 1 >= 0 and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == StoneDeposit:
        prob += 0.05
        solo = False

    # below left
    if y + 1 < config.world_size[1] and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == StoneDeposit:
        prob += 0.05
        solo = False

    # below right
    if y + 1 < config.world_size[1] and x + 1 < config.world_size[1] and type(vp.item_layer[y][x+1]) == StoneDeposit:
        prob += 0.05
        solo = False

    if solo:
        prob -=  0.0001 * s

    if prob > random.random():
        vp.item_layer[y][x] = StoneDeposit(x, y, vp, random.randint(50, 150))


def generate_trees(vp, x, y, s):
    prob = 0.0025

    # above
    if y - 1 >= 0 and type(vp.item_layer[y-1][x])  == Tree:
        prob += 0.075
        solo = False

    # below
    if y + 1 < config.world_size[1] and type(vp.item_layer[y+1][x])  == Tree:
        prob += 0.075
        solo = False

    # left
    if x - 1 >= 0 and type(vp.item_layer[y][x-1])  == Tree:
        prob += 0.075
        solo = False

    # right
    if x + 1< config.world_size[0] and type(vp.item_layer[y][x+1])  == Tree:
        prob += 0.075
        solo = False

    # above right
    if y - 1 >= 0 and x + 1 < config.world_size[0] and type(vp.item_layer[y][x+1]) == Tree:
        prob += 0.075
        solo = False

    # above left
    if y - 1 >= 0 and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == Tree:
        prob += 0.075
        solo = False

    # below left
    if y + 1 < config.world_size[1] and x - 1 >= 0 and type(vp.item_layer[y][x-1]) == Tree:
        prob += 0.075
        solo = False

    # below right
    if y + 1 < config.world_size[1] and x + 1 < config.world_size[1] and type(vp.item_layer[y][x+1]) == Tree:
        prob += 0.075
        solo = False

    if prob > random.random():
        vp.item_layer[y][x] = Tree(x, y, vp)
