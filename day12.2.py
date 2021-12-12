import sys
import itertools
from queue import Queue

class GraphBuilder:

    def __init__(self):
        self.verts = {}

    def make_vert(self, v):
        if v not in self.verts:
            self.verts[v] = {'prev': '', "id": v, "visit_count": 0, "can_visit": True, "neighbors": []}
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
    initcts = init_visit_counts(g.verts)
    cnt = get_paths(g.verts['start'], False)
    return cnt

def init_visit_counts(verts):
    cts = {}
    for k in verts:
        cts[k] = 0
    return cts

def is_invalid(v, sm_lock):
    vcount = v['visit_count']
    if v['id'] == 'start':
        return vcount > 0, sm_lock
    elif v['id'] == 'end':
        return False, sm_lock
    elif v['id'].isupper():
        return False, sm_lock
    # else:
    if not sm_lock: # allow double count for small
        if vcount == 1:
            return False, True # lock enabled
        else:
            return False, False # lock not yet enabled
    else:
        return v['id'].islower() and v['visit_count'] > 0 and v['id'] != 'end', sm_lock

def get_paths(v, sm_lock, prev=None):
    invalid, sm_lock = is_invalid(v, sm_lock)
    if invalid: #(v, sm_lock):
        return 0
    else:
        v['visit_count'] += 1

    if v['id'] == 'end':
        return 1

    cnt = 0
    for n in v['neighbors']:
        cnt += get_paths(n, sm_lock)
    v['visit_count'] -= 1
    return cnt

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
