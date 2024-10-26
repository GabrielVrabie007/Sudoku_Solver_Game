from Grid import *
import sys
import random
from Backtracking import *
from Constraint_propagation import *
from Measures import *


def generate_random_sudoku():
    """Generate a random Sudoku puzzle by filling the board and removing some cells."""

    def fill_board(board):
        """Recursively fill the board using backtracking."""
        empty = find_empty(board)
        if not empty:
            return True
        row, col = empty

        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if is_valid(board, num, row, col):
                board[row][col] = num
                if fill_board(board):
                    return True
                board[row][col] = 0

        return False

    def remove_numbers(board, attempts=40):
        """Remove numbers from a filled board to create a puzzle with some empty cells."""
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            board[row][col] = 0
            attempts -= 1

    # Generate a fully filled board
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)

    # Remove numbers to create a playable puzzle
    remove_numbers(board)

    return board


def main():
    # Generate an initial random board
    initial_board = generate_random_sudoku()
    grid = Grid(initial_board)
    selected = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Check if algorithm button is clicked
                if pos[1] > SCREEN_SIZE + BUTTON_HEIGHT:
                    selected_algo = grid.select_algo(pos)
                    if selected_algo:
                        # Generate a new random board for the new algorithm
                        new_board = generate_random_sudoku()
                        grid.reset_board(new_board)

                        if selected_algo == "Backtracking":
                            solve_with_backtracking(grid)
                        elif selected_algo == "Constraint Propagation":
                            solve_with_constraint_propagation(grid)
                        elif selected_algo == "Dancing Links (DLX)":
                            # Add the function call for Dancing Links here if implemented
                            pass

                # Check if number button is clicked
                elif SCREEN_SIZE <= pos[1] <= SCREEN_SIZE + BUTTON_HEIGHT:
                    grid.select_number(pos)

                # Otherwise, try to place the number on the grid
                else:
                    selected = grid.highlight_cell(pos)
                    if selected and grid.selected_number:
                        grid.place_number(pos, grid.selected_number)

        grid.draw_grid()
        grid.draw_numbers()
        grid.draw_number_buttons()
        grid.draw_algo_buttons()

        pygame.display.update()


if __name__ == "__main__":
    main()
