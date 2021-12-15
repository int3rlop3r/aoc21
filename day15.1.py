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
        print(total_risk, "+", val, '=', total_risk+val)
        total_risk += val

        if coord == endcoord:
            print("found the end!")
            q.task_done()
            break

        nodes = get_neighbors(grid, coord)
        # print(nodes)
        scores = defaultdict(int)
        for no in nodes:
            scores[no['coord']] += no['val'] 
            neighs = get_neighbors(grid, no['coord'])
            for n in neighs:
                scores[no['coord']] += n['val']
        if scores[nodes[0]['coord']] == scores[nodes[1]['coord']]:
            # print("equal", scores)
            minval = min(nodes, key=lambda x: x['val'])
            nextco = minval['coord']
        else:
            nextco = min(scores, key=lambda x: scores[x])
        print("next coord:", nextco)
        q.put(nextco)
        q.task_done()
        # for n in nodes:
    return total_risk

def get_neighbors(grid, coord):
    coords = (
            (coord[0]+1, coord[1]),
            (coord[0], coord[1]+1),
        )
    neighs = []
    for newco in coords:
        n = get_coord(grid, newco)
        if not n:
            continue
        neighs.append(n)
    return neighs

def get_coord(grid, coord):
    try:
        x = {
            'coord': (coord[0], coord[1]),
            # could use 'get_val' here but who cares?
            'val': grid[coord[0]][coord[1]],
        }
    except IndexError:
        x = {}
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
