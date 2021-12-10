import sys

scoremap = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
closechars = [")", "]", "}", ">",]
openchars = ["(", "[", "{", "<",]

def get_illchar_score(fd):
    score = 0
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
            score += scoremap[ch] # illegal char found!
            break
    return score

def main(fd):
    print(get_illchar_score(fd))

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            main(f)
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
