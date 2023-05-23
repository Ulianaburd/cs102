import copy
import random
import typing as tp

import pygame
from pygame.locals import *

cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed
        self.grid = self.create_grid(True)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        is_playing = True
        while is_playing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_playing = False
            self.grid = self.get_next_generation()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            arr = []  # type: ignore
            for i in range(0, self.cell_height):
                arr.append([])
                for j in range(0, self.cell_width):
                    arr[i].append(random.randint(0, 1))
            return arr
        else:
            arr = []  # type: ignore
            for i in range(0, self.cell_height):
                arr.append([])
                for j in range(0, self.cell_width):
                    arr[i].append(0)
            return arr

    def draw_grid(self) -> None:
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                side_a = self.cell_size
                side_b = self.cell_size
                coordinate_x = x * self.cell_size
                coordinate_y = y * self.cell_size
                rectangle = (coordinate_x, coordinate_y, side_a, side_b)
                pygame.draw.rect(self.screen, color, rect=rectangle)

    def get_neighbours(self, cell: cell) -> Cells:
        neighbours_indexes = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        result = []
        for x, y in neighbours_indexes:
            x_tocheck = x + cell[1]
            y_tocheck = y + cell[0]
            if x_tocheck < 0 or x_tocheck >= self.cell_width or y_tocheck < 0 or y_tocheck >= self.cell_height:
                continue
            result.append(self.grid[y_tocheck][x_tocheck])
        return result

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.grid)
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                neighbours_count = sum(self.get_neighbours((y, x)))
                if neighbours_count not in (2, 3):
                    new_grid[y][x] = 0
                elif neighbours_count == 3:
                    new_grid[y][x] = 1
        return new_grid


if __name__ == "__main__":
    game = GameOfLife(640, 480, 40)
    game.run()
