from grid import *


def find_possibilities(board, row, col):
    if board[row][col] != 0:
        return set()  # If cell is not empty, return an empty set as no possibilities are needed.

    possible_numbers = set(range(1, 10))  # Start with all numbers as possibilities.

    # Remove numbers present in the same row
    for c in range(9):
        if board[row][c] in possible_numbers:
            possible_numbers.remove(board[row][c])

    # Remove numbers present in the same column
    for r in range(9):
        if board[r][col] in possible_numbers:
            possible_numbers.remove(board[r][col])

    # Remove numbers present in the same 3x3 block
    block_row_start = (row // 3) * 3
    block_col_start = (col // 3) * 3
    for r in range(block_row_start, block_row_start + 3):
        for c in range(block_col_start, block_col_start + 3):
            if board[r][c] in possible_numbers:
                possible_numbers.remove(board[r][c])

    return possible_numbers


def solve_with_backtracking(board):
    """ Solve the Sudoku puzzle using a backtracking algorithm. """
    find = find_empty(board)
    if not find:
        return True  # Puzzle solved
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(board, i, row, col):
            board[row][col] = i
            if solve_with_backtracking(board):
                return True
            board[row][col] = 0

    return False  # Trigger backtracking


def solve_with_constraint_propagation(board):
    possibilities = {(r, c): set(range(1, 10)) if board[r][c] == 0 else {board[r][c]}
                     for r in range(9) for c in range(9)}

    def eliminate_possibilities():
        updated = False
        for r in range(9):
            for c in range(9):
                if len(possibilities[(r, c)]) == 1:
                    val = next(iter(possibilities[(r, c)]))
                    if board[r][c] == 0:
                        board[r][c] = val  # Set the value on the board if it's not already set
                    peers = get_peers(r, c)
                    for (pr, pc) in peers:
                        if val in possibilities[(pr, pc)]:
                            possibilities[(pr, pc)].remove(val)
                            updated = True
                            if len(possibilities[(pr, pc)]) == 1:
                                # Recursively set the single possibility to the board
                                next_val = next(iter(possibilities[(pr, pc)]))
                                board[pr][pc] = next_val
        return updated

    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for num in possibilities[(r, c)]:
                        if is_valid(board, num, r, c):
                            board[r][c] = num
                            if solve_with_constraint_propagation(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    def is_valid(board, num, row, col):
        block_r = (row // 3) * 3
        block_c = (col // 3) * 3
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
            if board[block_r + i // 3][block_c + i % 3] == num:
                return False
        return True

    if all(len(possibilities[(r, c)]) == 1 for r in range(9) for c in range(9) if board[r][c] == 0):
        return True  # The board is solved if all cells are singles and valid.

    # Apply constraint propagation techniques first
    while eliminate_possibilities():
        if all(board[r][c] != 0 for r in range(9) for c in range(9)):
            return True  # Exit if the board is solved

    # If constraint propagation can't solve the puzzle, fall back to backtracking
    return backtrack()


def get_peers(row, col):
    block_r = (row // 3) * 3
    block_c = (col // 3) * 3
    peers = set([(row, i) for i in range(9)] + [(i, col) for i in range(9)]
                + [(block_r + i, block_c + j) for i in range(3) for j in range(3)])
    peers.discard((row, col))
    return peers


def solve_with_rule_based(board):
    changes_made = False
    possibilities = {(r, c): set(range(1, 10)) if board[r][c] == 0 else {board[r][c]}
                     for r in range(9) for c in range(9)}

    def apply_rule_based_techniques():
        updated = False
        updated |= find_naked_pairs()
        updated |= find_hidden_singles()
        return updated

    def find_naked_pairs():
        found = False
        for unit in get_all_units():
            pairs = {}
            for pos in unit:
                if len(possibilities[pos]) == 2:
                    p_tuple = tuple(possibilities[pos])
                    pairs.setdefault(p_tuple, []).append(pos)
            for p_tuple, positions in pairs.items():
                if len(positions) == 2:
                    for other_pos in unit:
                        if other_pos not in positions and p_tuple.issubset(possibilities[other_pos]):
                            original = possibilities[other_pos].copy()
                            possibilities[other_pos].difference_update(p_tuple)
                            if possibilities[other_pos] != original:
                                found = True
                                if len(possibilities[other_pos]) == 1:
                                    final_num = next(iter(possibilities[other_pos]))
                                    board[other_pos[0]][other_pos[1]] = final_num
                                    changes_made = True
        return found

    def find_hidden_singles():
        found = False
        for unit in get_all_units():
            for num in range(1, 10):
                positions = [pos for pos in unit if num in possibilities[pos]]
                if len(positions) == 1:
                    single_pos = positions[0]
                    if possibilities[single_pos] != {num}:
                        possibilities[single_pos] = {num}
                        board[single_pos[0]][single_pos[1]] = num
                        found = True
                        changes_made = True
        return found

    def get_all_units():
        units = []
        for i in range(9):
            units.append([(i, j) for j in range(9)])  # Rows
            units.append([(j, i) for j in range(9)])  # Columns
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                units.append([(r + dr, c + dc) for dr in range(3) for dc in range(3)])  # Blocks
        return units

    while apply_rule_based_techniques():
        if all(board[r][c] != 0 for r in range(9) for c in range(9)):
            return True  # Puzzle solved using rule-based techniques

    # If there are still empty cells, fall back on backtracking
    return solve_with_backtracking(board) if any(board[r][c] == 0 for r in range(9) for c in range(9)) else True
