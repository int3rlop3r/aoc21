import sys

def get_power(fd):
    state = []
    for l in fd:
        increment_state(state, l.strip())
    gama = calculate_gama(state)
    epsln = calcualte_epsilon(state)
    return bin_to_dec(gama) * bin_to_dec(epsln)

def bin_to_dec(binlist):
    decimal = 0
    for d in binlist:
        decimal = decimal*2 + d
    return decimal

def increment_state(state, line):
    for i, c in enumerate(line):
        if len(state) <= i:
            state.append([0, 0])
        # check digit and incr
        if int(c) == 0:
            state[i][0] += 1
        else:
            state[i][1] += 1

def calculate_gama(state):
    digits = []
    for z, o in state:
        if z > o:
            digits.append(0)
        else:
            digits.append(1)
    return digits

def calcualte_epsilon(state):
    digits = []
    for z, o in state:
        if z < o:
            digits.append(0)
        else:
            digits.append(1)
    return digits

def main(fd):
    print(get_power(fd))

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fname) as f:
            main(f)

