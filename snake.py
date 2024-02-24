from collections import deque
from enum import Enum
import pygame
import program
import colours
import random

class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

class Node(Enum):
    EMPTY = 0
    APPLE = 1
    SNAKE = 2

class Snake:
    def __init__(self, size: int):
        self._grid_size = size
        self._start_pos = (size // 2, size // 2)
        self._node_size = program.WINDOW_SIZE // size
        self._snake = deque()
        self._grid = None
        self._dir = None
        self._prev_dir = None
        self._apple_pos = None

        self.restart()

    def restart(self) -> None:
        self._snake.clear()
        self._grid = [[Node.EMPTY for _ in range(self._grid_size)] for _ in range(self._grid_size)]
        self._dir = Direction.UP
        self._prev_dir = Direction.UP

        self._snake.append(self._start_pos)
        self.set_node_snake(self._start_pos)

        self.spawn_apple()

    def set_direction(self, direction: Direction) -> None:
        # Opposite directions have the same parites
        if (direction.value % 2) == (self._prev_dir.value % 2):
            return

        self._dir = direction

    def move(self) -> None:
        front = self._snake[-1]

        match self._dir:
            case Direction.UP:
                new_pos = (front[0] - 1, front[1])
            case Direction.DOWN:
                new_pos = (front[0] + 1, front[1])
            case Direction.LEFT:
                new_pos = (front[0], front[1] - 1)
            case _:  # Direction.RIGHT
                new_pos = (front[0], front[1] + 1)

        self._prev_dir = self._dir

        if not self.pos_in_grid(new_pos) or self.node_is_snake(new_pos):
            return self.restart()

        if self.node_is_apple(new_pos):
            self._snake.append(new_pos)
            self.set_node_snake(new_pos)

            self.spawn_apple()
        else:
            back = self._snake.popleft()
            self.set_node_empty(back)

            self._snake.append(new_pos)
            self.set_node_snake(new_pos)

    def spawn_apple(self) -> None:
        while True:
            empty_node_pos = []
            for r, row in enumerate(self._grid):
                for c, node in enumerate(row):
                    if node == Node.EMPTY:
                        empty_node_pos.append((r, c))

            r, c = random.choice(empty_node_pos)

            if self._grid[r][c] == Node.EMPTY:
                self._grid[r][c] = Node.APPLE
                self._apple_pos = (r, c)
                break

    def set_node_empty(self, pos: (int, int)) -> None:
        self._grid[pos[0]][pos[1]] = Node.EMPTY

    def set_node_snake(self, pos: (int, int)) -> None:
        self._grid[pos[0]][pos[1]] = Node.SNAKE

    def node_is_apple(self, pos: (int, int)) -> bool:
        return self._grid[pos[0]][pos[1]] == Node.APPLE

    def node_is_snake(self, pos: (int, int)) -> bool:
        return self._grid[pos[0]][pos[1]] == Node.SNAKE

    def pos_in_grid(self, pos: (int, int)) -> bool:
        return (0 <= pos[0] < self._grid_size) and (0 <= pos[1] < self._grid_size)

    def draw(self) -> None:
        self.draw_apple()
        self.draw_snake()

    def draw_snake(self) -> None:
        for pos in self._snake:
            self.draw_node(pos, colours.GREEN)

    def draw_apple(self) -> None:
        self.draw_node(self._apple_pos, colours.RED)

    def draw_node(self, pos: (int, int), colour: pygame.Color) -> None:
        render_rect = pygame.Rect(
            pos[1] * self._node_size + 5,
            pos[0] * self._node_size + 5,
            self._node_size - 10,
            self._node_size - 10
        )
        pygame.draw.rect(program.SURF, colour, render_rect)

    def size(self) -> int:
        return self._grid_size
