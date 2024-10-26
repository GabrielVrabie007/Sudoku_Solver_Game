from test_4 import *


def solve_with_backtracking(grid):
    def find_empty(board):
        # Find an empty cell in the board
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == 0:
                    return i, j
        return None

    def is_valid(board, num, row, col):
        # Check if the number is valid in the given row, column, and 3x3 grid
        for i in range(GRID_SIZE):
            if board[row][i] == num or board[i][col] == num:
                return False

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def backtrack(board):
        empty = find_empty(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if is_valid(board, num, row, col):
                board[row][col] = num
                if backtrack(board):
                    return True
                board[row][col] = 0
        return False

    # Solve the Sudoku puzzle using backtracking
    backtrack(grid.board)
