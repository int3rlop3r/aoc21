import sys

def gen_measures(fd):
    start, mid, end = [int(next(fd)) for i in range(3)]
    yield sum((start, mid, end))
    for l in fd:
        start = mid
        mid = end
        end = int(l)
        yield sum((start, mid, end))

def gen_events(fd):
    gen = gen_measures(fd)
    prev = next(gen)
    for l in gen:
        curr = int(l)
        if curr > prev:
            ev = 'increased'
        elif curr < prev:
            ev = 'decreased'
        else:
            ev = 'unchanged'
        yield prev, curr, ev
        prev = curr

def main(fd):
    inc = [i for i in gen_events(fd) if i[2] == 'increased']
    print(len(inc))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
