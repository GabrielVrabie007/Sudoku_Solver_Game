import pygame
from Measures import *
import random
from Backtracking import *
from Constraint_propagation import *
from inter import screen, user_font, font


class Grid:
    def __init__(self, board=None):
        self.original_board = [row[:] for row in board] if board else [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.board = [row[:] for row in self.original_board]
        self.selected_number = None
        self.user_inputs = set()
        self.hint_mode = False
        self.move_stack = []
        self.redo_stack = []
        self.algo_buttons = ["Backtracking", "Constraint Propagation", "Dancing Links (DLX)"]
        self.selected_algo = None
        self.possibilities = self.initialize_possibilities()

    def generate_random_board(self, num_clues=25):
        self.board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.user_inputs.clear()
        self.solve_board_with_backtracking()
        self.remove_random_cells(num_clues)
        self.original_board = [row[:] for row in self.board]
        self.possibilities = self.initialize_possibilities()

    def solve_board_with_backtracking(self):
        """Helper function to solve the board using backtracking."""
        empty = find_empty(self.board)
        if not empty:
            return True
        row, col = empty

        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if is_valid(self.board, num, row, col):
                self.board[row][col] = num
                if self.solve_board_with_backtracking():
                    return True
                self.board[row][col] = 0
        return False

    def remove_random_cells(self, num_clues):
        total_cells = GRID_SIZE * GRID_SIZE
        cells_to_remove = total_cells - num_clues

        while cells_to_remove > 0:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

    def reset_board(self, difficulty="medium"):
        num_clues = {"easy": 35, "medium": 25, "hard": 20}.get(difficulty, 25)
        self.generate_random_board(num_clues)
        self.user_inputs.clear()
        self.move_stack.clear()
        self.redo_stack.clear()
        self.possibilities = self.initialize_possibilities()

    def draw_grid(self):
        screen.fill(WHITE)
        for x in range(0, SCREEN_SIZE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_SIZE), 1)
            pygame.draw.line(screen, BLACK, (0, x), (SCREEN_SIZE, x), 1)
        for x in range(0, SCREEN_SIZE, CELL_SIZE * 3):
            pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_SIZE), 2)
            pygame.draw.line(screen, BLACK, (0, x), (SCREEN_SIZE, x), 2)

    def draw_numbers(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] != 0:
                    color = USER_INPUT_COLOR if (row, col) in self.user_inputs else BLACK
                    text = user_font.render(str(self.board[row][col]), True, color)
                    screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 8))

    def highlight_cell(self, pos):
        if pos[0] < SCREEN_SIZE and pos[1] < SCREEN_SIZE:
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 5)
            return row, col
        return None

    def draw_number_buttons(self):
        for i in range(9):
            button_rect = pygame.Rect(i * CELL_SIZE, SCREEN_SIZE, CELL_SIZE, BUTTON_HEIGHT)
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
            text = font.render(str(i + 1), True, WHITE)
            screen.blit(text, (i * CELL_SIZE + CELL_SIZE // 3, SCREEN_SIZE + BUTTON_HEIGHT // 5))
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect, 2)

        if self.selected_number:
            pygame.draw.rect(screen, USER_INPUT_COLOR,
                             (self.selected_number * CELL_SIZE - CELL_SIZE, SCREEN_SIZE, CELL_SIZE, BUTTON_HEIGHT), 3)

    def select_number(self, pos):
        if SCREEN_SIZE <= pos[1] <= SCREEN_SIZE + BUTTON_HEIGHT:
            col = pos[0] // CELL_SIZE
            self.selected_number = col + 1
            return self.selected_number
        return None

    def place_number(self, pos, selected_number):
        if pos[0] < SCREEN_SIZE and pos[1] < SCREEN_SIZE and selected_number is not None:
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            if (row, col) in self.user_inputs or self.board[row][col] == 0:
                previous = self.board[row][col]
                self.board[row][col] = 0 if previous == selected_number else selected_number
                if previous == 0:
                    self.user_inputs.add((row, col))
                elif self.board[row][col] == 0:
                    self.user_inputs.discard((row, col))
                self.move_stack.append((row, col, previous, selected_number))
                self.redo_stack.clear()

    def undo(self):
        if self.move_stack:
            row, col, old, new = self.move_stack.pop()
            self.redo_stack.append((row, col, self.board[row][col], old))
            self.board[row][col] = old
            if old == 0:
                self.user_inputs.discard((row, col))
            else:
                self.user_inputs.add((row, col))

    def redo(self):
        if self.redo_stack:
            row, col, old, new = self.redo_stack.pop()
            self.move_stack.append((row, col, self.board[row][col], new))
            self.board[row][col] = new
            if new == 0:
                self.user_inputs.discard((row, col))
            else:
                self.user_inputs.add((row, col))

    def draw_algo_buttons(self):
        for i, algo in enumerate(self.algo_buttons):
            button_x = i * (SCREEN_SIZE // len(self.algo_buttons))
            button_y = SCREEN_SIZE + BUTTON_HEIGHT
            button_width = SCREEN_SIZE // len(self.algo_buttons)
            button_rect = pygame.Rect(button_x, button_y, button_width, ALGO_BUTTON_HEIGHT)
            pygame.draw.rect(screen, ALGO_BUTTON_COLOR, button_rect)
            text = font.render(algo, True, WHITE)
            screen.blit(text, (button_x + 10, button_y + 5))
            if self.selected_algo is not None and self.selected_algo == i:
                pygame.draw.rect(screen, USER_INPUT_COLOR, button_rect, 3)
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, ALGO_BUTTON_HOVER_COLOR, button_rect, 2)

    def select_algo(self, pos):
        if SCREEN_SIZE + BUTTON_HEIGHT <= pos[1] <= TOTAL_HEIGHT:
            col = pos[0] // (SCREEN_SIZE // len(self.algo_buttons))
            if self.selected_algo is None or self.selected_algo != col:
                self.selected_algo = col
                self.reset_board()  # Clear and generate a new random board when a new algorithm is selected
                print(f"Selected Algorithm: {self.algo_buttons[col]}")
            return self.algo_buttons[col]
        return None

    def initialize_possibilities(self):
        possibilities = {}
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 0:
                    possibilities[(row, col)] = set(range(1, 10))
                else:
                    possibilities[(row, col)] = set()
        return possibilities

    def update_possibilities(self):
        # Update the possibilities for all cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 0:
                    self.possibilities[(row, col)] = self.find_possibilities(row, col)
                else:
                    self.possibilities[(row, col)] = set()

    def find_possibilities(self, row, col):
        # Find the possible values for a cell
        if self.board[row][col] != 0:
            return set()

        possible_values = set(range(1, 10))

        # Eliminate values based on the row
        for i in range(GRID_SIZE):
            if self.board[row][i] in possible_values:
                possible_values.remove(self.board[row][i])

        # Eliminate values based on the column
        for i in range(GRID_SIZE):
            if self.board[i][col] in possible_values:
                possible_values.remove(self.board[i][col])

        # Eliminate values based on the 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] in possible_values:
                    possible_values.remove(self.board[i][j])

        return possible_values
