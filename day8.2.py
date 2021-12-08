import sys
from collections import defaultdict

def get_dig_counts(fd):
    total = 0
    for l in fd:
        sigtxt, digtxt = l.split('|')
        number = get_number(sigtxt, digtxt)
        total += number
    return total

def get_number(sigtxt, digtxt):
    # print(sigtxt, "\n", digtxt)
    digmap = get_digmap(sigtxt)
    s = ""
    for dig in digtxt.split():
        d = set(dig)
        for k, v in digmap.items():
            if d != set(k):
                continue
            s += str(digmap[k])
    return int(s)

def get_digmap(sigtxt):
    digmap = {}
    cntmap = defaultdict(list)
    for i in sigtxt.split():
        dig = i.strip()
        if len(dig) == 2:
            digmap[dig] = 1
        elif len(dig) == 3:
            digmap[dig] = 7
        elif len(dig) == 4:
            digmap[dig] = 4
        elif len(dig) == 7:
            digmap[dig] = 8
        cntmap[len(dig)].append(dig)
    """
    2len5, 2&1->1, 2&7->2, 2&4->2, 2&8->5
    5len5, 5&1->1, 5&7->2, 5&4->3, 5&8->5
    3len5, 3&1->2, 3&7->3, 3&4->3, 3&8->5

    6len6, 6&1->1, 6&7->2, 6&4->3, 6&8->6
    9len6, 9&1->2, 9&7->3, 9&4->4, 9&8->6
    0len6, 0&1->2, 0&7->3, 0&4->3, 0&8->6
    """
    one = set(cntmap[2][0])
    # seven = cntmap[3][0]
    four = set(cntmap[4][0])
    # eight = cntmap[7][0]
    for dig in cntmap[5]:
        if len(set(dig) & one) == 2:
            digmap[dig] = 3
        elif len(set(dig) & four) == 2:
            digmap[dig] = 2
        else:
            digmap[dig] = 5

    for dig in cntmap[6]:
        if len(set(dig) & one) == 1:
            digmap[dig] = 6
        elif len(set(dig) & four) == 4:
            digmap[dig] = 9
        else:
            digmap[dig] = 0
    return digmap

def main(fd):
    print(get_dig_counts(fd))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
