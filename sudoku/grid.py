import random

DIFFICULTY_SETTINGS = {
    'Easy': 40,
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
    initial_positions = [(row, col) for row in range(9) for col in range(9) if board[row][col] != 0]
    return board, initial_positions


def is_valid(board, num, row, col):
    block_row, block_col = (row // 3) * 3, (col // 3) * 3

    for i in range(9):
        if board[row][i] == num:
            print(f"Invalid due to row conflict at ({row}, {i})")
            return False
        if board[i][col] == num:
            print(f"Invalid due to column conflict at ({i}, {col})")
            return False

    for i in range(3):
        for j in range(3):
            if board[block_row + i][block_col + j] == num:
                print(f"Invalid due to block conflict at ({block_row + i}, {block_col + j})")
                return False

    return True


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None
