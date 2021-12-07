import sys
from collections import Counter

def calc_fuel(pos):
    records = {}
    min_fuel = None
    for p in pos:
        fuel = 0
        for l in pos:
            fuel += abs(l - p)
        records[p] = fuel
        if min_fuel == None:
            min_fuel = fuel
        elif fuel < min_fuel:
            min_fuel = fuel
    # return records
    return min_fuel


def main(fd):
    pos = [int(i) for i in fd.read().split(",")]
    print(calc_fuel(pos))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
