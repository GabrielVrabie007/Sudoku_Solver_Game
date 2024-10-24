import pygame


def solve_with_backtracking(grid):
    empty = find_empty(grid.board)
    if not empty:
        return True  # Puzzle solved
    row, col = empty

    for num in range(1, 10):
        if is_valid(grid.board, num, row, col):
            grid.board[row][col] = num
            grid.user_inputs.add((row, col))
            grid.draw_grid()
            grid.draw_numbers()
            pygame.display.update()
            pygame.time.wait(50)  # Visualize with delay

            if solve_with_backtracking(grid):
                return True

            grid.board[row][col] = 0
            grid.user_inputs.remove((row, col))
            grid.draw_grid()
            grid.draw_numbers()
            pygame.display.update()
            pygame.time.wait(50)  # Visualize with delay

    return False


def is_valid(board, num, row, col):
    # Check row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None
