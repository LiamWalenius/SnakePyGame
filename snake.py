from collections import deque
from enum import Enum
from dataclasses import dataclass
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

@dataclass(frozen=True)
class Position:
    r: int
    c: int

class Snake:
    def __init__(self, size: int):
        self._grid_size = size
        self._start_pos = Position(size // 2, size // 2)
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
        # Opposite directions have the same parities
        if (direction.value % 2) == (self._prev_dir.value % 2):
            return

        self._dir = direction

    def move(self) -> None:
        front = self._snake[-1]

        match self._dir:
            case Direction.UP:
                new_pos = Position(front.r - 1, front.c)
            case Direction.DOWN:
                new_pos = Position(front.r + 1, front.c)
            case Direction.LEFT:
                new_pos = Position(front.r, front.c - 1)
            case _:  # Direction.RIGHT
                new_pos = Position(front.r, front.c + 1)

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
        empty_node_pos = []
        for r, row in enumerate(self._grid):
            for c, node in enumerate(row):
                if node == Node.EMPTY:
                    empty_node_pos.append(Position(r, c))

        self._apple_pos = random.choice(empty_node_pos)
        self.set_node_apple(self._apple_pos)

    def set_node_empty(self, pos: Position) -> None:
        self._grid[pos.r][pos.c] = Node.EMPTY

    def set_node_apple(self, pos: Position) -> None:
        self._grid[pos.r][pos.c] = Node.APPLE

    def set_node_snake(self, pos: Position) -> None:
        self._grid[pos.r][pos.c] = Node.SNAKE

    def node_is_apple(self, pos: Position) -> bool:
        return self._grid[pos.r][pos.c] == Node.APPLE

    def node_is_snake(self, pos: Position) -> bool:
        return self._grid[pos.r][pos.c] == Node.SNAKE

    def pos_in_grid(self, pos: Position) -> bool:
        return (0 <= pos.r < self._grid_size) and (0 <= pos.c < self._grid_size)

    def pos_to_window_coords(self, pos: Position) -> (int, int):
        return (
            pos.c * self._node_size,
            pos.r * self._node_size
        )

    def draw(self) -> None:
        self.draw_snake()
        self.draw_apple()

    def draw_snake(self) -> None:
        if len(self._snake) == 1:
            return self.draw_node(self._snake[0], colours.GREEN)

        padding = 5

        for i in range(1, len(self._snake)):
            x1, y1 = self.pos_to_window_coords(self._snake[i-1])
            x2, y2 = self.pos_to_window_coords(self._snake[i])

            top_left_x = min(x1, x2)
            top_left_y = min(y1, y2)

            bottom_right_x = max(x1, x2) + self._node_size
            bottom_right_y = max(y1, y2) + self._node_size

            render_rect = pygame.Rect(
                top_left_x + padding,
                top_left_y + padding,
                bottom_right_x - top_left_x - padding*2,
                bottom_right_y - top_left_y - padding*2
            )
            pygame.draw.rect(program.SURF, colours.GREEN, render_rect)

    def draw_apple(self) -> None:
        self.draw_node(self._apple_pos, colours.RED)

    def draw_node(self, pos: Position, colour: pygame.Color) -> None:
        padding = 5

        x, y = self.pos_to_window_coords(pos)

        render_rect = pygame.Rect(
            x + padding,
            y + padding,
            self._node_size - padding*2,
            self._node_size - padding*2
        )
        pygame.draw.rect(program.SURF, colour, render_rect)
