import sys

def parse_line(l):
    direction, units = l.split()
    return direction, int(units)

# just indexes
hor = 0
ver = 1
def get_pos(fd):
    # prev = int(next(fd))
    pos = [0, 0]
    for l in fd:
        direction, units = parse_line(l)
        if direction == "forward":
            pos[hor] += units
        elif direction == "up":
            pos[ver] -= units
        elif direction == "down":
            pos[ver] += units
    return pos[hor] * pos[ver]

def main(fd):
    # inc = [i for i in gen_events(fd) if i[2] == 'increased']
    print(get_pos(fd))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
