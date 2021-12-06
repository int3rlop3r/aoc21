import sys
import re
import itertools
from collections import defaultdict
from pprint import pprint

def calc_fish_population(fish, days):
    fish_count = defaultdict(int)
    for f in fish:
        fish_count[f] += 1

    population = count_all(fish_count, days)
    return population.values()

def count_all(fish_count, days):
    if not days:
        return fish_count

    total_count = defaultdict(int)
    for f, c in fish_count.items():
        if f == 0:
            total_count[6] += c
            total_count[8] += c
        else:
            total_count[f-1] += c
    return count_all(total_count, days-1)

def main(fd):
    fish = [int(i) for i in fd.read().split(',')]
    print(sum(calc_fish_population(fish, 256)))

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fname) as f:
            main(f)
