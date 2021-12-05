import sys
from pprint import pprint

def bingo(fd):
    numb = [int(i) for i in next(fd).split(",")]
    _ = next(fd) # blank line
    boards = []
    board = []
    for l in fd:
        if l == "\n":
            boards.append(board.copy())
            board = []
            continue
        rows = []
        for n in l.split():
            rows.append({"mark": 0, "numb": int(n)})
        board.append(rows.copy())
    boards.append(board.copy())

    # start playing
    bid, won_by, number = -1, -1, -1
    for i, n in enumerate(numb):
        call_number(n, boards) # [2]])
        bid, won_by = check_winner(boards) # [boards[2]])
        if bid != -1:
            number = n
            break
    return get_score(boards[bid], won_by, number)

def get_score(board, won_by, num_called):
    score = 0
    for row in board:
        for col in row:
            if col['mark'] == 1:
                continue
            score += col['numb']
    return score*num_called

def call_number(num, boards):
    for bid, board in enumerate(boards):
        for rid, row in enumerate(board):
            for cid, col in enumerate(row):
                if num != col["numb"]:
                    continue
                col["mark"] = 1

def check_winner(boards):
    for bid, board in enumerate(boards):
        rscore = [0]*5
        cscore = [0]*5
        for rid, row in enumerate(board):
            for cid, col in enumerate(row):
                if col["mark"] != 1:
                    continue
                rscore[rid] += 1 # col["numb"]
                cscore[cid] += 1 # col["numb"]
        x = 5
        rfound = rscore.index(x) if x in rscore else -1
        cfound = cscore.index(x) if x in cscore else -1
        if rfound != -1:
            return bid, ("row", rfound)
        elif cfound != -1:
            return bid, ("col", cfound)
    return -1, (-1, -1)

def print_board(board):
    for r in board:
        for c in r:
            if c['mark'] == 1:
                print(c['numb'], "*", end=' ')
            else:
                print(c['numb'], " ", end=' ')
        print()

def main(fd):
    print(bingo(fd))

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f"python {sys.argv[0]} <input_file.txt>")
    else:
        with open(fname) as f:
            main(f)
