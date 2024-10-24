import pygame
from Measures import GRID_SIZE


def solve_with_constraint_propagation(grid):
    grid.update_possibilities()  # Initialize possibilities

    # Apply elimination and only choice until no more progress can be made
    while True:
        progress = False

        # Elimination: if a cell has a number, remove that number from the possibilities of other cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid.board[row][col] != 0:
                    num = grid.board[row][col]
                    # Eliminate this number from the possibilities of the row, column, and box
                    progress |= eliminate_possibilities(grid, num, row, col)

        # Only Choice: if a number can only go in one cell in a row, column, or box, place it there
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid.board[row][col] == 0:
                    possibilities = grid.possibilities[(row, col)]
                    if len(possibilities) == 1:
                        num = possibilities.pop()
                        grid.board[row][col] = num
                        grid.user_inputs.add((row, col))
                        progress = True

                        # Update the screen to show progress
                        grid.draw_grid()
                        grid.draw_numbers()
                        pygame.display.update()
                        pygame.time.wait(50)  # Visualize delay

        # If no progress is made, break the loop
        if not progress:
            break

    # Return True if the board is solved, otherwise False
    return all(grid.board[row][col] != 0 for row in range(GRID_SIZE) for col in range(GRID_SIZE))


def eliminate_possibilities(grid, num, row, col):
    progress = False
    # Eliminate from the row
    for i in range(GRID_SIZE):
        if (row, i) in grid.possibilities and num in grid.possibilities[(row, i)]:
            grid.possibilities[(row, i)].remove(num)
            progress = True

    # Eliminate from the column
    for i in range(GRID_SIZE):
        if (i, col) in grid.possibilities and num in grid.possibilities[(i, col)]:
            grid.possibilities[(i, col)].remove(num)
            progress = True

    # Eliminate from the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i, j) in grid.possibilities and num in grid.possibilities[(i, j)]:
                grid.possibilities[(i, j)].remove(num)
                progress = True

    return progress
