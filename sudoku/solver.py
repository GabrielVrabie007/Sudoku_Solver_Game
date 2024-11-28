from grid import *
import pygame
import sys


def solve_with_backtracking(board, screen, draw_grid, font, delay):
    print("Starting backtracking...")  # Debugging entry
    empty = find_empty(board)
    if not empty:
        print("Puzzle solved!")
        return True

    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            draw_grid(screen, font, board, None)
            pygame.display.update()
            pygame.time.delay(delay)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        delay = max(10, delay - 10)  # Speed up
                        print(f"Fast forwarding, new delay: {delay}")
                    elif event.key == pygame.K_s:
                        delay = 0  # Skip delay
                        print("Skipping to end...")

            if solve_with_backtracking(board, screen, draw_grid, font, delay):
                return True

            board[row][col] = 0
            draw_grid(screen, font, board, None)
            pygame.display.update()

    return False


def solve_with_constraint_propagation(board, screen, draw_grid, font, delay=100):
    from itertools import product, combinations

    def is_valid(board, num, row, col):
        block_row, block_col = (row // 3) * 3, (col // 3) * 3
        return all(num != board[row][x] for x in range(9)) and \
               all(num != board[y][col] for y in range(9)) and \
               all(num != board[block_row + y // 3][block_col + y % 3] for y in range(9))

    def find_possibilities():
        possibilities = {}
        for row, col in product(range(9), repeat=2):
            if board[row][col] == 0:
                possible = set(range(1, 10))
                block_row, block_col = (row // 3) * 3, (col // 3) * 3
                for k in range(9):
                    possible.discard(board[row][k])
                    possible.discard(board[k][col])
                    possible.discard(board[block_row + k // 3][block_col + k % 3])
                possibilities[(row, col)] = possible
        return possibilities

    def apply_naked_pairs(possibilities):
        units = define_units()
        for unit in units:
            # Filter cells in the unit that exist in possibilities and have exactly two possibilities
            pairs = [(cell, possibilities[cell]) for cell in unit if
                     cell in possibilities and len(possibilities[cell]) == 2]
            for (cell1, poss1), (cell2, poss2) in combinations(pairs, 2):
                if poss1 == poss2:
                    # Remove these possibilities from other cells in the unit
                    for cell in unit:
                        if cell in possibilities and cell != cell1 and cell != cell2:
                            possibilities[cell] -= poss1

    def define_units():
        row_units = [list(product([r], range(9))) for r in range(9)]
        column_units = [list(product(range(9), [c])) for c in range(9)]
        box_units = [list(product(range(br, br + 3), range(bc, bc + 3)))
                     for br in range(0, 9, 3) for bc in range(0, 9, 3)]
        return row_units + column_units + box_units

    def apply_constraints():
        possibilities = find_possibilities()
        apply_naked_pairs(possibilities)
        changed = False
        for (row, col), possible in possibilities.items():
            if len(possible) == 1:
                board[row][col] = possible.pop()
                changed = True
                draw_grid(screen, font, board, None)
                pygame.display.update()
                pygame.time.delay(delay)
        return changed

    def is_solved():
        return all(board[row][col] != 0 for row in range(9) for col in range(9))

    def backtrack():
        if is_solved():
            return True
        possibilities = find_possibilities()
        if not possibilities:
            return False
        # Find the cell with the least number of possibilities
        cell, possible = min(possibilities.items(), key=lambda x: len(x[1]))
        row, col = cell
        for num in possible:
            if is_valid(board, num, row, col):
                board[row][col] = num
                draw_grid(screen, font, board, None)
                pygame.display.update()
                pygame.time.delay(delay)
                if backtrack():
                    return True
                board[row][col] = 0
                draw_grid(screen, font, board, None)
                pygame.display.update()
        return False

    # Apply constraints as far as possible; if unsolved, fallback to backtracking
    while apply_constraints():
        if is_solved():
            return True
    return backtrack()


def solve_with_rule_based(board, screen, draw_grid, font, delay=100):
    from itertools import product, combinations

    def is_valid(board, num, row, col):
        block_row, block_col = (row // 3) * 3, (col // 3) * 3
        return all(num != board[row][x] for x in range(9)) and \
               all(num != board[y][col] for y in range(9)) and \
               all(num != board[block_row + y // 3][block_col + y % 3] for y in range(9))

    def find_possibilities():
        possibilities = {}
        for row, col in product(range(9), repeat=2):
            if board[row][col] == 0:
                possible = set(range(1, 10))
                block_row, block_col = (row // 3) * 3, (col // 3) * 3
                for k in range(9):
                    # Check for potential out-of-bounds access
                    possible.discard(board[row][k])
                    possible.discard(board[k][col])
                    if 0 <= block_row + k // 3 < 9 and 0 <= block_col + k % 3 < 9:
                        possible.discard(board[block_row + k // 3][block_col + k % 3])
                possibilities[(row, col)] = possible
        return possibilities

    def apply_rules(possibilities):
        changed = False
        for (row, col), possible in list(possibilities.items()):
            if len(possible) == 1:
                num = possible.pop()
                if is_valid(board, num, row, col):
                    board[row][col] = num
                    changed = True
                    draw_grid(screen, font, board, None)
                    pygame.display.update()
                    pygame.time.delay(max(10, delay))
        return changed

    def fallback_backtracking():
        def backtrack():
            empty = [(row, col) for row, col in product(range(9), repeat=2) if board[row][col] == 0]
            if not empty:
                return True
            row, col = empty[0]
            for num in range(1, 10):
                if is_valid(board, num, row, col):
                    board[row][col] = num
                    draw_grid(screen, font, board, None)
                    pygame.display.update()
                    pygame.time.delay(max(10, delay))
                    if backtrack():
                        return True
                    board[row][col] = 0
            return False

        print("Falling back to backtracking.")  # Debugging
        return backtrack()

    iteration = 0
    max_iterations = 500  # Limit iterations to avoid infinite loop

    while True:
        iteration += 1
        if iteration > max_iterations:
            print("Max iterations reached, switching to backtracking.")  # Debugging
            return fallback_backtracking()

        print(f"Iteration {iteration}: Solving with rule-based algorithm.")  # Debugging

        possibilities = find_possibilities()
        if not possibilities:
            print("No possibilities left. Exiting.")  # Debugging
            break

        progress = apply_rules(possibilities)
        if not progress:
            if all(board[row][col] != 0 for row, col in product(range(9), repeat=2)):
                print("Puzzle solved with rule-based algorithm.")  # Debugging
                return True
            else:
                return fallback_backtracking()

