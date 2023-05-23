# coding: utf-8
import copy
import pathlib
import random
from typing import List, Optional, Tuple

cell = Tuple[int, int]
cells = List[int]
grid = List[cells]


class GameOfLife:
    def __init__(
        self,
        size: Tuple[int, int],
        random: bool = True,
        max_gen: Optional[int] = None,
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=random)
        self.max_generations = max_gen
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> grid:
        if randomize:
            arr = []
            for i in range(0, self.rows):
                arr.append([])
                for j in range(0, self.cols):
                    arr[i].append(random.randint(0, 1))
            return arr
        else:
            arr = []
            for i in range(0, self.rows):
                arr.append([])
                for j in range(0, self.cols):
                    arr[i].append(0)
            return arr

    def get_neighbours(self, cell: cell) -> cells:
        neighbours = [
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
        for x, y in neighbours:
            xx = x + cell[1]
            yy = y + cell[0]
            if (xx < 0 or xx >= self.cols) or (yy < 0 or yy >= self.rows):
                continue
            result.append(self.curr_generation[yy][xx])
        return result

    def get_next_generation(self) -> grid:
        current_grid = copy.deepcopy(self.curr_generation)
        for y in range(self.rows):
            for x in range(self.cols):
                neighbours_count = sum(self.get_neighbours((y, x)))
                if neighbours_count not in (2, 3):
                    current_grid[y][x] = 0
                elif neighbours_count == 3:
                    current_grid[y][x] = 1
        return current_grid

    def step(self) -> None:
        new_gen = self.get_next_generation()
        self.prev_generation = self.curr_generation
        self.curr_generation = new_gen
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations:
            if self.generations >= self.max_generations:
                return True
            else:
                return False
        else:
            return False

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        grid = []
        with open(filename) as f:
            lines = f.readlines()
            height = len(lines)
            arr = []
            for i in lines[0]:
                if i.isdigit():
                    arr.append(i)
            width = len(arr)
            for line in lines:
                new_row = []
                for i in line:
                    if i.isdigit():
                        new_row.append(int(i))
                grid.append(new_row)
        life = GameOfLife((height, width), random=False)
        life.curr_generation = copy.deepcopy(grid)
        return life

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join([str(el) for el in row]))
                f.write("\n")
