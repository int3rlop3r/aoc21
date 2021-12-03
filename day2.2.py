import sys

# just indexes
hor = 0
ver = 1
aim = 2
def get_pos(fd):
    # prev = int(next(fd))
    pos = [0, 0, 0]
    for l in fd:
        direction, units = parse_line(l)
        if direction == "forward":
            forward(pos, units) # [hor] += units
        elif direction == "up":
            pos[aim] -= units
        elif direction == "down":
            pos[aim] += units
    return pos[hor] * pos[ver]

def parse_line(l):
    direction, units = l.split()
    return direction, int(units)

def forward(pos, units):
    pos[hor] += units
    pos[ver] += (pos[aim] * units)

def main(fd):
    # inc = [i for i in gen_events(fd) if i[2] == 'increased']
    print(get_pos(fd))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
