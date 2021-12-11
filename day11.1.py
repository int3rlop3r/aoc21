import sys
import itertools
from collections import deque
from queue import Queue

def get_flash_count(fd, days):
    grid = make_grid(fd)
    # print_grid(grid)
    flashes = 0
    for day in range(days):
        # print("day:", day+1)
        grid = step(grid)
        flashes += sum(1 for i in itertools.chain.from_iterable(grid) if i == 0)
        # print_grid(grid)
        # print()
    return flashes

def step(grid):
    grid, flash_coords = incr_and_flash(grid)
    q = Queue()
    for c in flash_coords:
        q.put(c)

    # for flashco in q:
    visited = set()
    while not q.empty():
        flashco = q.get()
        if flashco in visited:
            # print("visited:", flashco)
            q.task_done()
            continue
        else:
            visited.add(flashco)
        submatrix = get_submatrix(grid, flashco)
        new_sm, sub_flashcos = incr_and_flash(submatrix, is_step=False)
        apply_submatrix(new_sm, grid, flashco)
        for flc in sub_flashcos:
            d = dirs[flc[0]][flc[1]]
            newco = cofunc[d](flashco)
            if not is_valid_point(newco, grid):
                continue
            q.put(newco)
        q.task_done()
    return grid

def apply_submatrix(submatrix, grid, point):
    for r, c, elem in iter_grid(submatrix):
        d = dirs[r][c]
        newco = cofunc[d](point)
        if not is_valid_point(newco, grid):
            continue
        grid[newco[0]][newco[1]] = elem

cofunc = {
        "topleft": lambda coord: (coord[0]-1, coord[1]-1),
        "top": lambda coord: (coord[0]-1, coord[1]),
        "topright": lambda coord: (coord[0]-1, coord[1]+1),
        "left": lambda coord: (coord[0], coord[1]-1),
        "curr": lambda coord: (coord[0], coord[1]),
        "right": lambda coord: (coord[0], coord[1]+1),
        "downleft": lambda coord: (coord[0]+1, coord[1]-1),
        "down": lambda coord: (coord[0]+1, coord[1]),
        "downright": lambda coord: (coord[0]+1, coord[1]+1),
}
dirs = (
    ("topleft", "top", "topright"),
    ("left", "curr", "right"),
    ("downleft", "down", "downright"),
)

def get_submatrix(grid, coord):
    r = 0
    c = 1
    submatr = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    for d in itertools.chain.from_iterable(dirs):
        p = cofunc[d](coord)
        sp = cofunc[d]((1, 1))
        if not is_valid_point(p, grid):
            # print("skipping:", d)
            continue
        try:
            submatr[sp[r]][sp[c]] = grid[p[r]][p[c]]
        except IndexError:
            print("="*50)
            print("sp", sp)
            print("p", p)
            raise
    return submatr

def is_valid_point(point, grid):
    r = 0
    c = 1
    if -1 in point:
        # print("skipping:", d)
        return False
    elif point[r] > len(grid)-1 or point[c] > len(grid[0])-1:
        # print("skipping:", d)
        return False
    return True

def iter_grid(grid):
    for r, row, in enumerate(grid):
        for c, col in enumerate(row):
            yield r, c, col

def incr_and_flash(grid, is_step=True):
    flash_coords = []
    ng = [0]*len(grid)


    for r, c, elem in iter_grid(grid):
        if not is_step and elem > 0: # if elem > 0: # skip -1s
            elem += 1
        elif is_step:
            elem += 1

        if elem > 9:
            elem = 0
            flash_coords.append((r, c))

        if not ng[r]:
            ng[r] = []
        ng[r].append(elem)
    return ng, flash_coords

def make_grid(fd):
    grid = []
    for l in fd:
        grid.append([int(c) for c in l.strip()])
    return grid

def print_grid(grid):
    for r in grid:
        # print("".join(r))
        for i in r:
            print(i, end="")
        print()
    print()

def main(fd):
    print(get_flash_count(fd, 100))

if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fpath) as f:
            main(f)
