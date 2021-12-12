import sys
import itertools
from queue import Queue

class GraphBuilder:

    def __init__(self):
        self.verts = {}

    def make_vert(self, v):
        if v not in self.verts:
            self.verts[v] = {"id": v, "visit_count": 0, "can_visit": True, "neighbors": []}
        return self.verts[v]

    def bind(self, x, y):
        """coz it adds an edge both ways"""
        vertx = self.make_vert(x)
        verty = self.make_vert(y)
        vertx['neighbors'].append(verty)
        verty['neighbors'].append(vertx)

def count_cave_paths(fd, days):
    g = GraphBuilder()
    for line in fd:
        fr, to = line.strip().split('-')
        g.bind(fr, to)
    cnt = get_paths(g.verts['start'])
    return cnt

def get_paths(v):
    if is_invalid(v):
        return 0
    else:
        v['visit_count'] += 1

    if v['id'] == 'end':
        return 1

    cnt = 0
    for n in v['neighbors']:
        cnt += get_paths(n)
    v['visit_count'] = 0
    return cnt

def is_invalid(v):
    return v['id'].islower() and v['visit_count'] > 0 and v['id'] != 'end'

def main(fd):
    print(count_cave_paths(fd, 100))

if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fpath) as f:
            main(f)
