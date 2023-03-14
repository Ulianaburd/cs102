import pathlib
import typing as tp
from random import randint

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    res = []
    for j in range(int(len(values) / n)):
        tmp = []
        for i in range(n):
            tmp.append(values[j * n + i])
        res.append(tmp)

    return res


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    res = []

    for t in grid:
        res.append(t[pos[1]])

    return res


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    cell = [0, 0]

    cell[0] = pos[0] // 3
    cell[1] = pos[1] // 3

    res = []
    for j in range(3 * cell[0], 3 * cell[0] + 3):
        for i in range(3 * cell[1], 3 * cell[1] + 3):
            res.append(grid[j][i])

    return res


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    r = (0, 0)
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            if grid[j][i] == ".":
                r = (j, i)
                return r
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)

    pos_row = []
    pos_col = []
    pos_block = []

    for d in "123456789":
        if d not in row:
            pos_row.append(d)

    for d in "123456789":
        if d not in col:
            pos_col.append(d)

    for d in "123456789":
        if d not in block:
            pos_block.append(d)

    res = []
    for t in pos_row:
        if t in pos_col and t in pos_block:
            res.append(t)

    return set(res)


def solve(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    pos = find_empty_positions(grid)
    if pos is None:
        return grid
    else:
        values = find_possible_values(grid, pos)
        if len(values) == 0:
            return grid
        for t in values:
            grid[pos[0]][pos[1]] = t
            grid = solve(grid)
            if not find_empty_positions(grid):
                return grid
            grid[pos[0]][pos[1]] = "."
        return grid


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    for i in range(9):
        pos = (0, i)
        test = get_col(solution, pos)
        for d in "123456789":
            if d not in test:
                return False

        pos = (i, 0)
        test = get_row(solution, pos)
        for d in "123456789":
            if d not in test:
                return False

        pos = ((i * 3) % 9, (i * 3) // 9)
        test = get_block(solution, pos)
        for d in "123456789":
            if d not in test:
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [["." for i in range(9)] for j in range(9)]
    grid = solve(grid)
    if N > 81:
        N = 81
    for i in range(81 - N):
        x, y = randint(0, 8), randint(0, 8)
        while grid[x][y] == ".":
            x, y = randint(0, 8), randint(0, 8)
        grid[x][y] = "."
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
