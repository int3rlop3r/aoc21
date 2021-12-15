import sys
from collections import defaultdict
from queue import Queue

# def get_val(grid, coord):
get_val = lambda grid, coord: grid[coord[0]][coord[1]]

def get_risk_cnt(fd): 
    grid = make_grid(fd)
    # print_grid(grid)
    q = Queue()
    startcoord = (0, 0)
    endcoord = (len(grid)-1, len(grid[0])-1)
    # cost = get_val(grid, startcoord)
    cost = 0 # starting position is never entered so risk isn't calculated

    q.put((startcoord, (), cost))
    # print(endcoord)
    table = {} # { (0, 0): {"prev": (), "cost:" get_val((0, 0))} }
    while not q.empty():
        coord, prev, cost = q.get()
        print("popping", coord)
        if coord not in table:
            table[coord] = {'cost': cost, 'prev': prev}

        if table[coord]['cost'] > cost:
            table[coord] = {'cost': cost, 'prev': prev}

        # val = get_val(grid, coord)
        # print(total_risk, "+", val, '=', total_risk+val)
        # total_risk += val
        # if coord == endcoord:
            # print("found the end!")
            # q.task_done()
            # break

        neighs = get_neighbors(grid, coord)
        for ncoor, ncost in sorted((n for n in neighs if n), key=lambda x: x[1]):
            print("putting ncoor", ncoor)
            if ncoor not in table:
                q.put((ncoor, coord, ncost+cost)) # neighbor coordinates
            elif ncost+cost < table[ncoor].get('cost', 0):
                q.put((ncoor, coord, ncost+cost)) # neighbor coordinates

        # print(sns)
        # m = min(neighs, key=lambda x: x[1])
        # print(neighs)
        # print(m)
        # for n in neighs:

        # q.put(nextco)
        q.task_done()
        # for n in nodes:
    print(table)
    return cost

def get_neighbors(grid, coord):
    coords = (
            (coord[0]+1, coord[1]), # move right
            (coord[0], coord[1]+1), # move down
        )
    neighs = []
    for newco in coords:
        n = get_coord(grid, newco)
        if n[1] is None: # 0 could be a valid cost!
            continue
        neighs.append(n)
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
            print(i, end="")
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
