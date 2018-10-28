from VersionA.System import *
import pygame
from pygame.locals import *
import time

test = System(40, 40, 0)

test.add_heat([0, 0], 2400)
test.add_heat([0, 39], 2400)
test.add_heat([39, 0], 2400)
test.add_heat([39, 39], 2400)

SCREEN_SIZE = (600, 600)

screen = pygame.display.set_mode(SCREEN_SIZE)

clock = pygame.time.Clock()
clock.tick(60)

alive = True


def clamp(mi, ma, value):
    return min(ma, max(value, mi))


def mix(min, min_color, max, max_color, value):
    diff = max - min
    max_weight = clamp(0, 1, (value - min) / diff)
    min_weight = 1 - max_weight
    return (
        int(min_color[0] * min_weight + max_color[0] * max_weight),
        int(min_color[1] * min_weight + max_color[1] * max_weight),
        int(min_color[2] * min_weight + max_color[2] * max_weight),
    )


def handle_events():
    global alive
    for event in pygame.event.get():
        if event.type == QUIT:
            alive = False


def draw():
    screen.fill((0, 0, 0))
    for w in range(test.width):
        for h in range(test.height):
            color = mix(1, (0, 0, 255), 25, (255, 0, 0), test.grid[w][h])
            pygame.draw.rect(screen, color, (w*16, h*16, 16, 16))
    pygame.display.flip()


def update():
    test.apply_entropy(1.0/60.0)

while alive:
    handle_events()
    draw()
    update()


