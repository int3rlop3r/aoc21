import sys
import itertools
from collections import defaultdict

def get_polymer_res(fd, steps=40):
    seq = next(fd).strip()
    tpl = get_tpl(fd)
    mc = defaultdict(int)
    cts = init_counts(seq, mc)
    for i in range(steps):
        cts = step_new(cts, tpl, mc)
    maxkey = max(mc, key=lambda x: mc[x])
    minkey = min(mc, key=lambda x: mc[x])
    return mc[maxkey] - mc[minkey]

def render_string(groups):
    string = []
    for g, c in groups.items():
        string += list(set(g)) * c
    return string

def step_new(cts, tpl, mc):
    new_cts = defaultdict(int)
    for k, v in cts.items():
        ch = tpl.get(k)
        if not ch:
            continue
        mc[ch] = mc[ch] + 1 * v
        part1, part2 = k[0]+ch, ch+k[1]
        # print(k, '->', ch, part1, part2, v)
        new_cts[part1] = new_cts[part1] + 1 * v
        new_cts[part2] = new_cts[part2] + 1 * v
    # print('-----')
    return new_cts

def init_counts(seq, mc):
    d = defaultdict(int)
    prev = ""
    for s in seq:
        mc[s] += 1
        if not prev:
            prev = s
            continue
        d[prev+s] += 1
        prev = s
    return d

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
