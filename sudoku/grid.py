import random

DIFFICULTY_SETTINGS = {
    'Easy': 40,  # Number of cells to pre-fill
    'Medium': 30,
    'Hard': 20
}


def generate_board(difficulty='Easy'):
    base = 3
    side = base * base

    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    def shuffle(s): return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, side + 1))
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares - DIFFICULTY_SETTINGS[difficulty]
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board


def is_valid(board, guess, row, col):
    if guess in board[row]:
        return False
    if guess in (board[i][col] for i in range(9)):
        return False
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    if guess in (board[r][c] for r in range(startRow, startRow + 3) for c in range(startCol, startCol + 3)):
        return False
    return True


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None
