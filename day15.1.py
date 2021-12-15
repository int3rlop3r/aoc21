import sys
from collections import defaultdict
from queue import Queue

# def get_val(grid, coord):
get_val = lambda grid, coord: grid[coord[0]][coord[1]]

def iter_grid(grid):
    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            yield r, c, elem

def get_risk_cnt(fd): 
    grid = make_grid(fd)
    # print_grid(grid)
    start = (0, 0)
    table = {start: {'prev': (), 'cost': 0, 'currval': 1}}
    endcoord = (len(grid)-1, len(grid[0])-1)
    count = 0
    for r, c, elem in iter_grid(grid):
        curr = (r, c)
        # if curr == start:
            # # skip start
            # continue
        neighs = get_neighbors(grid, curr) # get_neighbors_reverse
        print(curr, neighs)
        # curr_cost = table[curr]['cost']
        if len(neighs) == 0: # will never happen now
            continue

        # ncoor = selected[0] # coors are in '0'
        for ncoor, nval in neighs:
            if curr not in table:
                table[curr] = {
                    'cost': nval+elem,
                    'prev': ncoor,
                    'currval': elem,
                }
            # ncost = table[ncoor]['cost']
            newcost = table[curr]['cost']+elem
            if table[curr]['cost'] > newcost:
                table[curr] = {
                    'cost': newcost,
                    'prev': ncoor,
                    'currval': elem,
                }
    # return table[endcoord]['cost']
    from pprint import pprint
    pprint(table)

def set_cost(curr, elem, ncoor, table):
    # ncoor = neigh # selected[0] # coors are in '0'
    ncost = table[ncoor]['cost']
    cost = elem+ncost
    if curr in table and table[curr]['cost'] < cost:
        return # continue
    table[curr] = {'cost': cost, 'prev': ncoor, 'currval': elem}

def get_neighbors_reverse(grid, coord):
    coords = (
            (coord[0]-1, coord[1]), # move up
            (coord[0], coord[1]-1), # move left
        )
    neighs = []
    for newco in coords:
        n = get_coord(grid, newco)
        if n[1] is None or any(i < 0 for i in newco): # 0 could be a valid cost!
            continue
        neighs.append(n)
    return neighs # first up then left

def get_neighbors(grid, coord):
    coords = (
            (coord[0]-1, coord[1]), # move up
            (coord[0]+1, coord[1]), # move down
            (coord[0], coord[1]-1), # move left
            (coord[0], coord[1]+1), # move right
        )
    neighs = []
    for newco in coords:
        n = get_coord(grid, newco)
        # if n[1] is None: # 0 could be a valid cost!
        if n[1] is None or any(i < 0 for i in newco): # 0 could be a valid cost!
            continue
        neighs.append(n)
    return neighs # up, down, left, right

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
        # fmt = "{:>2}"*len(r)
        # print(fmt.format(r))
        for i in r:
            print(i, end=" ")
        print()
    print()

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
