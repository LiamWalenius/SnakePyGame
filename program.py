import sys
import pygame
from pygame.locals import *
import colours
import snake

WINDOW_SIZE = 800
SURF = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

FPS = 60
FRAME_COUNTER = pygame.time.Clock()
# Time between updates in milliseconds
UPDATE_TIME = 250
UPDATE_EVENT = pygame.event.custom_type()
pygame.time.set_timer(UPDATE_EVENT, UPDATE_TIME)

GRID_SIZE = 15
GAME = snake.Snake(GRID_SIZE)

def init():
    pygame.init()
    pygame.display.set_caption('Snake')

    while True:
        handle_events()
        render()

        FRAME_COUNTER.tick(FPS)

def handle_events():
    from snake import Direction

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == UPDATE_EVENT:
            update()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w]:
            GAME.set_direction(Direction.UP)
        if pressed_keys[K_s]:
            GAME.set_direction(Direction.DOWN)
        if pressed_keys[K_a]:
            GAME.set_direction(Direction.LEFT)
        if pressed_keys[K_d]:
            GAME.set_direction(Direction.RIGHT)

def update():
    GAME.move()

def render():
    SURF.fill(colours.BLACK)
    GAME.draw()
    pygame.display.update()
