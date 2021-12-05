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

    bid, won_by = -1, -1
    exclude_id = []
    exclude = []
    number = []
    for i, n in enumerate(numb):
        call_number(n, boards, exclude_id) # [2]])
        winners = check_winner(boards, exclude_id) # [boards[2]])
        if len(winners) == 0:
            continue
        for w in winners:
            exclude_id.append(w[0])
            exclude.append(boards[w[0]])
            number.append(n)
    print_board(exclude[-1])
    return get_score(exclude[-1], won_by, number[-1])

def get_score(board, won_by, num_called):
    score = 0
    for row in board:
        for col in row:
            if col['mark'] == 1:
                continue
            score += col['numb']
        print("score:", score)
    return score*num_called

def call_number(num, boards, exclude):
    for bid, board in enumerate(boards):
        if bid in exclude:
            continue
        for rid, row in enumerate(board):
            for cid, col in enumerate(row):
                if num != col["numb"]:
                    continue
                col["mark"] = 1

def check_winner(boards, exclude):
    winners = []
    for bid, board in enumerate(boards):
        if bid in exclude:
            continue
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
            winners.append((bid, ("row", rfound)))
        elif cfound != -1:
            winners.append((bid, ("col", cfound)))
    return winners

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
