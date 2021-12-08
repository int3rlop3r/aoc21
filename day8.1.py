import sys
from collections import Counter, defaultdict

def get_dig_counts(fd):
    c = Counter()
    for l in fd:
        sigtxt, digtxt = l.split('|')
        c.update(len(i.strip()) for i in digtxt.split())
    scnt = defaultdict(int, c)
    # 1s + 4s + 7s + 8s
    # 2seg + 4seg + 3seg + 7seg
    return scnt[2] + scnt[4] + scnt[3] + scnt[7]

def main(fd):
    print(get_dig_counts(fd))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
