import sys
import re
import itertools
from pprint import pprint

patt = re.compile("(\d+),(\d+) -> (\d+),(\d+)")
x = 0
y = 1
e = 2
def get_overlap(fd):
    coors = []
    maxx = 0
    maxy = 0
    for l in fd:
        start, end = parse_line(l)
        if start[x] == end[x]:
            ev = "samex"
        elif start[y] == end[y]:
            ev = "samey"
        else:
            continue
        coors.append((start, end, ev))
        maxx, maxy = get_max(maxx, maxy, start, end)
    display = init_display(maxx, maxy)
    for coor in coors:
        plot(display, coor)

    print_board(display)
    return get_sum(display)

def get_sum(display):
    total = 1
    return sum(total for i in itertools.chain.from_iterable(display) if i > 1)

def print_board(display):
    for row in display:
        print(row)

def plot(display, coor):
    if coor[e] == "samex":
        start = coor[0][y]
        end = coor[1][y]
        if start > end:
            start, end = end, start
        for i in range(start, end+1):
            try:
                display[i][coor[0][x]] += 1
            except IndexError:
                print("len:", len(display[i]), "i", i, "x:", coor[0][x])
                print("error")
                raise
    else:
        start = coor[0][x]
        end = coor[1][x]
        if start > end:
            start, end = end, start
        for i in range(start, end+1):
            try:
                display[coor[0][y]][i] += 1
            except IndexError:
                print("len:", len(display[i]), "i", i, "y:", coor[0][y])
                print("error")
                raise

def init_display(maxx, maxy):
    display = [0]*(maxy+1)
    for i in range(len(display)):
        display[i] = [0]*(maxx+1)
    return display

def get_max(maxx, maxy, start, end):
    maxx = max(maxx, start[x], end[x])
    maxy = max(maxy, start[y], end[y])
    return maxx, maxy

def parse_line(line):
    sx, sy, ex, ey = patt.match(line).groups()
    return (int(sx), int(sy)), (int(ex), int(ey))

def main(fd):
    print(get_overlap(fd))

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fname) as f:
            main(f)
