from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]



def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:

    y, x = coord
    direction = choice([0, 1])  # 0 is up, 1 is right
    if direction == 0:
        if y == 1 and x != len(grid) - 2:
            grid[y][x + 1] = " "
        elif y == 1 and x == len(grid) - 2:  #  случай, если мы попадаем в угол
            pass
        else:
            grid[y - 1][x] = " "
    else:
        if x == len(grid) - 2 and y != 1:
            grid[y - 1][x] = " "
        elif x == len(grid) - 2:
            pass
        else:
            grid[y][x + 1] = " "

    return grid

def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            remove_wall(grid, (x, y))

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:

    return [(x, y) for x, row in enumerate(grid) for y, cell in enumerate(row) if cell == "X"]


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:

    for x, y in [(x1, y1) for x1, row in enumerate(grid) for y1, cell in enumerate(row) if cell == k]:
        for coord in [
            xy
            for xy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if 0 <= xy[0] < len(grid) and 0 <= xy[1] < len(grid[0])
        ]:
            if grid[coord[0]][coord[1]] == 0:
                grid[coord[0]][coord[1]] = k + 1
    return grid


def shortest_path(grid: List[List[Union[str, int]]], exit: Tuple[int, int]) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:

    k = grid[exit[0]][exit[1]]
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]

    if k == 1:
        return [exit]
    k_f = int(k) - 1
    for x, y in [
        xy
        for xy in [(exit[0] - 1, exit[1]), (exit[0] + 1, exit[1]), (exit[0], exit[1] - 1), (exit[0], exit[1] + 1)]
        if 0 <= xy[0] < len(grid) and 0 <= xy[1] < len(grid[0])
    ]:

        if grid[x][y] == k_f:
            path = shortest_path(grid, (x, y))
            if path is not None and len(path) == k_f and isinstance(path, list):
                return [exit] + path
            else:
                grid[x][y] = " "
    return None


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:

    corners = {(0, 0), (len(grid) - 1, len(grid[0]) - 1), (0, len(grid[0]) - 1), (len(grid) - 1, 0)}
    if coord in corners:
        return True

    xy_check: Optional[Tuple[int, int]]
    xy_check = None

    if coord[0] == 0:
        xy_check = (coord[0] + 1, coord[1])
    elif coord[0] == len(grid) - 1:
        xy_check = (coord[0] - 1, coord[1])
    elif coord[1] == 0:
        xy_check = (coord[0], coord[1] + 1)
    elif coord[1] == len(grid[0]) - 1:
        xy_check = (coord[0], coord[1] - 1)

    if xy_check is not None:
        if grid[xy_check[0]][xy_check[1]] == "■":
            return True
        return False

    if grid[coord[0]][coord[1]] == "■":
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]]
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:

    grid_copy = deepcopy(grid)

    exits = get_exits(grid_copy)
    if encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
        return grid, None

    grid_copy[exits[0][0]][exits[0][1]] = 1
    grid_copy[exits[1][0]][exits[1][1]] = 0

    for row in grid_copy:
        for y, _ in enumerate(row):
            if row[y] == " ":
                row[y] = 0
    k = 0
    while grid_copy[exits[1][0]][exits[1][1]] == 0:
        k = k + 1
        grid_copy = make_step(grid_copy, k)

    return grid, shortest_path(grid_copy, exits[1])


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


print(pd.DataFrame(bin_tree_maze(15, 15)))
GRID = bin_tree_maze(15, 15, False)
print(pd.DataFrame(GRID))
_, PATH = solve_maze(GRID)
MAZE = add_path_to_grid(GRID, PATH)
print(pd.DataFrame(MAZE))
