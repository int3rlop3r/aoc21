import sys

def get_power(fd):
    numb = []
    for l in fd:
        increment_state(numb, l.strip())
    oxy = calculate_oxy(numb)
    co2 = calculate_co2(numb)
    return bin_to_dec(oxy) * bin_to_dec(co2)

def increment_state(numb, line):
    for i, c in enumerate(line):
        if len(numb) <= i:
            numb.append([[], []])

        # check digit and incr
        if int(c) == 0:
            numb[i][0].append(line)
        else:
            numb[i][1].append(line)

def _pick_max(x, y, key=None):
    if len(x) > len(y):
        return x
    return y

def _pick_min(x, y, key=None):
    if len(y) < len(x):
        return y
    return x

def calculate_oxy(numb):
    return calculate(numb, _pick_max)

def calculate_co2(numb):
    return calculate(numb, _pick_min)

def calculate(numb, func):
    inter = []
    for curr_group in numb:
        if not inter:
            inter = func(*curr_group, key=len)
            continue
        inter0 = list(set(inter) & set(curr_group[0]))
        inter1 = list(set(inter) & set(curr_group[1]))

        inter = func(inter0, inter1, key=len)

        if len(inter) != 1:
            continue
        assert len(inter) == 1
        return inter[0]

def bin_to_dec(binlist):
    decimal = 0
    for d in binlist:
        decimal = decimal*2 + int(d)
    return decimal

def main(fd):
    print(get_power(fd))

if __name__ == '__main__':
    # x = [['011101110101', '000001010101'], ['001001010001', '001101011110']]
    # print(calculate_oxy(None, x))
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fname) as f:
            main(f)

