def solve_with_constraint_propagation(grid):
    def eliminate(possibilities, row, col, num):
        # Eliminate a number from the possibilities of the given cell
        if num in possibilities[(row, col)]:
            possibilities[(row, col)].remove(num)

    def only_choice(possibilities, row, col):
        # Check if there is only one choice left for a cell
        return len(possibilities[(row, col)]) == 1

    def reduce_possibilities(grid):
        # Apply constraint propagation by reducing possibilities for each cell
        changes = True
        while changes:
            changes = False
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if grid.board[row][col] == 0:
                        current_possibilities = grid.find_possibilities(row, col)
                        if len(current_possibilities) == 1:
                            # If there's only one possible number, fill it in
                            grid.board[row][col] = current_possibilities.pop()
                            grid.update_possibilities()
                            changes = True
                        else:
                            # Update the cell's possibilities
                            grid.possibilities[(row, col)] = current_possibilities

    # Solve the Sudoku puzzle using constraint propagation
    reduce_possibilities(grid)
