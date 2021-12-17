import sys
import itertools
from collections import defaultdict
from queue import Queue

# def get_val(grid, coord):
get_val = lambda grid, coord: grid[coord[0]][coord[1]]

def iter_grid(grid):
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            yield r, c, elem

def moddu(elem, i):
    x = (elem+i) % 9
    if x == 0:
        return 9
    return x

def grow_grid(grid):
    new_grid = []
    for i in range(5):
        for row in grid:
            row = [moddu(k, i) for k in row]
            new_row = []
            for j in range(5):
                # new_grid.append([moddu(col, j) for col in row])
                for col in row:
                    # print(moddu(col, j), end='  ')
                    new_row.append(moddu(col, j))
            # print()
            new_grid.append(new_row.copy())
    return new_grid


def get_risk_cnt(fd): 
    print("there is an off by 1 error somewhere!")
    grid = make_grid(fd)
    # new_grid = grow_grid(grid)
    grid = grow_grid(grid)
    table = {(0, 0): {'prev': (), 'cost': 0, 'currval': 1}}
    endcoord = (len(grid)-1, len(grid[0])-1)
    count = 0
    for r, c, elem in iter_grid(grid):
        curr = (r, c)
        # neigh = get_neighbors_reverse(grid, curr)
        neigh = get_neighbors(grid, curr, table)
        # curr_cost = table[curr]['cost']
        if len(neigh) == 0:
            continue
        elif len(neigh) == 1:
            selected = neigh[0]
        elif table[neigh[0][0]]['cost'] < table[neigh[1][0]]['cost']:
            #cost of left < up
            selected = neigh[0]
        elif table[neigh[1][0]]['cost'] <= table[neigh[0][0]]['cost']:
            #cost up < left
            selected = neigh[1]

        ncoor = selected[0] # coors are in '0'
        ncost = table[ncoor]['cost']
        cost = elem+ncost
        if curr in table and table[curr]['cost'] < cost:
            continue
        table[curr] = {'cost': cost, 'prev': ncoor, 'currval': elem}
    return table[endcoord]['cost'] - get_val(grid, (0, 0))
    # return table[endcoord]['cost']

def get_neighbors_reverse(grid, coord):
    coords = (
            (coord[0]-1, coord[1]), # move left
            (coord[0], coord[1]-1), # move up
        )
    neighs = []
    for newco in coords:
        n = get_coord(grid, newco)
        if n[1] is None or any(i < 0 for i in newco): # 0 could be a valid cost!
            continue
        neighs.append(n)
    return neighs # first left then up

def get_neighbors(grid, coord, table):
    coords = (
            (coord[0]-1, coord[1]), # move up
            (coord[0], coord[1]-1), # move left
            (coord[0]+1, coord[1]), # move down
            (coord[0], coord[1]+1), # move right
        )
    neighs = []
    for newco in coords:
        cost = 0
        if newco in table:
            cost = table[newco]['cost']
        n = get_coord(grid, newco)
        if n[1] is None: # 0 could be a valid cost!
            continue
        neighs.append(n[0], n[1]+cost)
    return neighs # first right then down

def get_coord(grid, coord):
    try:
        # x = {
            # 'coord': coord,
            # # could use 'get_val' here but who cares?
            # 'val': get_val(grid, coord),
        # }
        return coord, get_val(grid, coord)
    except IndexError:
        # x = {
            # 'coord': coord,
            # 'val': -1,
        # }
        return coord, None

def make_grid(fd):
    grid = []
    for line in fd:
        grid.append([int(i) for i in line.strip()])
    return grid


def print_grid(grid):
    for r in grid:
        # print("".join(r))
        for i in r:
            print(i, end=" ")
        print()
    print()

def make_row(row, i):
    new_row = []
    for nc in row:
        num = i + (nc % 9)
        new_row.append(num)
    return new_row

def main(fd):
    print(get_risk_cnt(fd))

if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fpath) as f:
            main(f)
