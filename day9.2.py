import sys
from functools import reduce
from queue import Queue

up = 0
down = 1
left = 2
right = 3

q = Queue()

def calc_risk(fd):
    hmap = make_hmap(fd)
    lows = get_lows(hmap)
    sizes = []
    for low in lows:
        bsize = get_basin_size(hmap, low)
        sizes.append(bsize)
    return reduce(lambda x, y: x * y, sorted(sizes)[-3:])

def get_basin_size(hmap, low):
    q.put(low)
    visited = []
    total = 0
    while not q.empty():
        coord = q.get()
        if coord not in visited:
            adjvals = get_adj(hmap, coord[0], coord[1])
            val = get_pos(hmap, coord[0], coord[1])
            total += 1
            for direc, value in enumerate(adjvals):
                if value in (9, None):
                    continue
                ncoord = get_next_coords(coord, direc)
                nval = get_pos(hmap, ncoord[0], ncoord[1])
                if not get_pos(hmap, ncoord[0], ncoord[1]):
                    continue
                q.put(ncoord)
        visited.append(coord)
        q.task_done()
    return total

def get_next_coords(curr, direc):
    return (
        (curr[0] - 1, curr[1]),
        (curr[0] + 1, curr[1]),
        (curr[0], curr[1] - 1),
        (curr[0], curr[1] + 1),
    )[direc]

def get_lows(hmap):
    lows = []
    for r, c, val in iter_hmap(hmap):
        adjvals = get_adj(hmap, r, c)
        if is_low(val, adjvals):
            lows.append((r, c))
    return lows

def is_low(middle, adjvals):
    return all(middle < i for i in adjvals if i is not None)

def get_adj(hmap, r, c):
    up = get_pos(hmap, r-1, c)
    down = get_pos(hmap, r+1, c)
    left = get_pos(hmap, r, c-1)
    right = get_pos(hmap, r, c+1)
    return (up, down, left, right)

def get_pos(hmap, row, col):
    #@TODO: club this into 1?
    if row < 0 or col < 0:
        return None

    try:
        return hmap[row][col]
    except IndexError:
        return None

def iter_hmap(hmap):
    for i, row in enumerate(hmap):
        for j, val in enumerate(row):
            yield i, j, val

def make_hmap(fd):
    heightmap = []
    for l in fd:
        heightmap.append([int(i) for i in l if i != '\n'])
    return heightmap

def main(fd):
    print(calc_risk(fd))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
