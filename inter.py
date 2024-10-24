import pygame
import sys

pygame.init()

SCREEN_SIZE = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
BUTTON_HEIGHT = 70
ALGO_BUTTON_HEIGHT = 40
TOTAL_HEIGHT = SCREEN_SIZE + BUTTON_HEIGHT + ALGO_BUTTON_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (173, 216, 230)
GRAY = (240, 240, 240)
USER_INPUT_COLOR = (255, 102, 0)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)
ALGO_BUTTON_COLOR = (80, 80, 80)
ALGO_BUTTON_HOVER_COLOR = (120, 120, 120)

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

screen = pygame.display.set_mode((SCREEN_SIZE, TOTAL_HEIGHT))
pygame.display.set_caption("Sudoku")
pygame.font.init()

font = pygame.font.SysFont("Arial", 24)
user_font = pygame.font.SysFont("Arial", 24, bold=True)


class Grid:
    def __init__(self, board):
        self.board = board
        self.selected_number = None
        self.user_inputs = set()
        self.algo_buttons = ["Backtracking", "Constraint Propagation", "Dancing Links (DLX)"]
        self.selected_algo = None

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
                    if (row, col) in self.user_inputs:
                        text = user_font.render(str(self.board[row][col]), True, USER_INPUT_COLOR)
                    else:
                        text = font.render(str(self.board[row][col]), True, BLACK)
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
        if pos[0] < SCREEN_SIZE and pos[1] < SCREEN_SIZE and selected_number:
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            if self.board[row][col] == 0:
                self.board[row][col] = selected_number
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
            self.selected_algo = col
            print(f"Selected Algorithm: {self.algo_buttons[col]}")
            return self.algo_buttons[col]
        return None


def main():
    grid = Grid(board)
    selected = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if pos[1] > SCREEN_SIZE + BUTTON_HEIGHT:
                    grid.select_algo(pos)
                elif pos[1] > SCREEN_SIZE:
                    grid.select_number(pos)
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
