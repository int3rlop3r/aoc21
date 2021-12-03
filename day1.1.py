import sys

def gen_events(fd):
    prev = int(next(fd))
    for l in fd:
        curr = int(l)
        if curr > prev:
            ev = 'increased'
        else:
            ev = 'decreased'
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
