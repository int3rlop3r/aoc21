import sys
import itertools

def print_product_code(fd):
    points, instrs = load_data(fd)
    for ins in instrs:
        points = fold_points(points, ins[0], ins[1])
    grid = plot(points)
    print_grid(grid)

def fold_points(points, axis, fold):
    new_points = []
    for pt in points:
        if axis == 'x':
            x, y = get_newx(fold, pt)
        else:
            x, y = get_newy(fold, pt)
        new_points.append((x, y))
    return new_points

def get_newx(fold, pt):
    # dup code
    oldx = pt[0]
    if fold > oldx:
        return pt
    units = oldx - fold
    newx = fold - units
    return newx, pt[1]

def get_newy(fold, pt):
    # dup code
    oldy = pt[1]
    if fold > oldy:
        return pt
    units = oldy - fold
    newy = fold - units
    return pt[0], newy

def load_data(fd):
    # load points
    pts = []
    for l in fd:
        if l == "\n":
            break
        x, y = l.strip().split(',')
        pts.append((int(x), int(y)))
    # loads instructions
    instrs = []
    for l in fd:
        txtins = l.strip().split()[-1]
        ax, pt = txtins.split('=')
        instrs.append((ax, int(pt)))
    return pts, instrs

def plot(points):
    grid = make_blank(points)
    for p in points:
        grid[p[1]][p[0]] = 1
    return grid

def print_grid(grid):
    for g in grid:
        print(''.join(str(i) for i in g))

def make_blank(points):
    maxx = maxy = 0
    for pt in points:
        maxx = max(pt[0], maxx)
        maxy = max(pt[1], maxy)
    maxx += 1
    maxy += 1
    grid = ['.']*maxy
    for i in range(maxy):
        grid[i] = [' ']*maxx
    return grid

def main(fd):
    print_product_code(fd)

if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fpath) as f:
            main(f)
