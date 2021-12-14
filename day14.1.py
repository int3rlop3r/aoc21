import sys
import itertools
from collections import Counter

def get_polymer_res(fd, steps=10): 
    seq = next(fd).strip()
    tpl = get_tpl(fd)
    for i in range(steps):
        prev = ""
        nseq = ""
        for s in seq:
            if not prev:
                nseq += s
                prev = s
                continue
            c = tpl.get(prev+s, "")
            nseq += c+s
            prev = s
        seq = nseq
    c = Counter(seq)
    maxkey = max(c, key=lambda x: c[x])
    minkey = min(c, key=lambda x: c[x])
    return c[maxkey] - c[minkey]

def get_tpl(fd):
    _ = next(fd) # blank line
    tpl = {}
    for l in fd:
        k = l[:2]
        v = l[-2]
        tpl[k] = v
    return tpl

def main(fd):
    print(get_polymer_res(fd))

if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fpath) as f:
            main(f)
