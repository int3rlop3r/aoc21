import sys

scoremap = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
closechars = [")", "]", "}", ">",]
openchars = ["(", "[", "{", "<",]

def get_illchar_score(fd):
    totals = []
    for line in fd:
        stack = []
        for ch in line:
            if ch == "\n":
                continue

            if ch in openchars:
                stack.append(ch)
                continue
            topidx = openchars.index(stack[-1])
            if closechars[topidx] == ch:
                stack.pop(-1)
                continue
            break # illegal char found!
        else:
            total = 0
            while len(stack):
                top = stack.pop(-1)
                topidx = openchars.index(top)
                closechar = closechars[topidx]
                total = calscore(total, closechar)
            totals.append(total)
    return sorted(totals)[int(len(totals)/2)]

def calscore(total, ch):
    return (total * 5) + scoremap[ch]

def main(fd):
    print(get_illchar_score(fd))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
