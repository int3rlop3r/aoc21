import sys

up = 0
down = 1
left = 2
right = 3

def calc_risk(fd):
    hmap = make_hmap(fd)
    risk = 0
    for r, c, val in iter_hmap(hmap):
        adjvals = get_adj(hmap, r, c)
        if is_low(val, adjvals):
            risk += (val+1) # add risk
    return risk

def is_low(middle, adjvals):
    return all(middle < i for i in adjvals if i is not None)

def get_adj(hmap, r, c):
    up = get_pos(hmap, r-1, c)
    down = get_pos(hmap, r+1, c)
    left = get_pos(hmap, r, c-1)
    right = get_pos(hmap, r, c+1)
    return tuple([up, down, left, right])

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
