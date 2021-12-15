import sys
from collections import defaultdict
from queue import Queue

# def get_val(grid, coord):
get_val = lambda grid, coord: grid[coord[0]][coord[1]]

def get_risk_cnt(fd): 
    grid = make_grid(fd)
    # print_grid(grid)
    q = Queue()
    q.put((0, 0))
    total_risk = 0
    endcoord = (len(grid)-1, len(grid[0])-1)
    print(endcoord)
    while not q.empty():
        coord = q.get()
        val = get_val(grid, coord)
        # print(total_risk, "+", val, '=', total_risk+val)
        total_risk += val

        if coord == endcoord:
            print("found the end!")
            q.task_done()
            break

        right_cost, right = get_right_cost(grid, coord)
        down_cost, down = get_down_cost(grid, coord)
        # print(right_cost, down_cost)
        if right_cost < down_cost:
            nextco = right
            print("go right")
        else:
            print("go down")
            nextco = down
        print("putting", nextco)
        q.put(nextco)
        q.task_done()
        # for n in nodes:
    return total_risk

def get_right_cost(grid, coords):
    c = (
            (coords[0], coords[1]+1),
            (coords[0], coords[1]+2),
            (coords[0]+1, coords[1]+1),
            (coords[0]+1, coords[1]+2),
        )
    return get_cost(grid, c), (coords[0], coords[1]+1)
    # return 1, (coords[0], coords[1]+1)

def get_down_cost(grid, coords):
    c = (
            (coords[0]+1, coords[1]),
            (coords[0]+2, coords[1]),
            (coords[0]+1, coords[1]+1),
            (coords[0]+2, coords[1]+1),
        )
    # return get_cost(grid, coords), coords[0]+1, coords[1]
    return get_cost(grid, c), (coords[0]+1, coords[1])

def get_cost(grid, coords):
    cost = 0
    for c in coords:
        data = get_coord(grid, c)
        cost += data['val']
    return cost

def get_coord(grid, coord):
    try:
        x = {
            'coord': (coord[0], coord[1]),
            # could use 'get_val' here but who cares?
            'val': grid[coord[0]][coord[1]],
        }
    except IndexError:
        x = {
            'coord': (coord[0], coord[1]),
            'val': 0,
        }
    return x

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
