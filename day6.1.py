import sys
import re
import itertools
from pprint import pprint

def calc_fish_population(fish, days):
    if not days:
        return fish

    new_fish = 0
    next_gen = []
    for f in fish:
        t = f - 1
        if t < 0:
            t = 6
            new_fish += 1
        next_gen.append(t)
    if new_fish:
        next_gen += [8]*new_fish
    return calc_fish_population(next_gen, days - 1)

def main(fd):
    fish = [int(i) for i in fd.read().split(',')]
    print(len(calc_fish_population(fish, 80)))

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fname) as f:
            main(f)
