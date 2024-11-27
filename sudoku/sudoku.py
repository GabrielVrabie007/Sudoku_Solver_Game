import pygame
import sys
from solver import *
from grid import *
from measures import *


def select_difficulty(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'Easy'
                elif event.key == pygame.K_2:
                    return 'Medium'
                elif event.key == pygame.K_3:
                    return 'Hard'

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        messages = ['Press 1 for Easy', 'Press 2 for Medium', 'Press 3 for Hard']
        for i, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (50, 150 + i * 50))
        pygame.display.update()


def display_message(screen, message, color=(255, 255, 255), duration=2000):
    """Displays a message on the screen for a short period."""
    font = pygame.font.Font(None, 36)  # Initialize font
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(duration)  # Display the message for 'duration' milliseconds


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Solver")
font = pygame.font.Font(None, 40)
algo_buttons = ["Backtracking", "Constraint", "Rule-based"]


def draw_grid(board, selected=None):
    for x in range(0, GRID_SIZE, BLOCK_SIZE):
        for y in range(0, GRID_SIZE, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
            value = board[y // BLOCK_SIZE][x // BLOCK_SIZE]
            if value != 0:
                text = font.render(str(value), True, (0, 128, 255))
                screen.blit(text, (x + 15, y + 10))
            if selected and selected == (y // BLOCK_SIZE, x // BLOCK_SIZE):
                pygame.draw.rect(screen, BUTTON_HIGHLIGHT_COLOR, rect, 3)


def draw_number_buttons(selected_number):
    x = GRID_SIZE + 10  # Positioning x to the right of the grid with a small gap
    y_start = 10  # A small top margin
    for number in range(1, 10):  # Numbers 1-9
        rect = pygame.Rect(x, y_start + (number - 1) * (BUTTON_HEIGHT + 10), BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, rect)  # Drawing the button
        if number == selected_number:
            pygame.draw.rect(screen, BUTTON_HIGHLIGHT_COLOR, rect, 2)  # Highlight selected number
        text = font.render(str(number), True, BUTTON_TEXT_COLOR)
        screen.blit(text, (rect.x + 30, rect.y + 5))


def draw_algorithm_buttons():
    start_x = (SCREEN_WIDTH - (3 * BUTTON_WIDTH + 2 * BUTTON_GAP)) // 2
    start_y = SCREEN_HEIGHT - BUTTON_AREA_HEIGHT + 10
    for idx, button in enumerate(algo_buttons):
        rect = pygame.Rect(start_x + idx * (BUTTON_WIDTH + BUTTON_GAP), start_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        text = font.render(button, True, BUTTON_TEXT_COLOR)
        screen.blit(text, (rect.x + 10, rect.y + 5))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Solver")
    font = pygame.font.Font(None, 40)
    algo_buttons = ["Backtracking", "Constraint", "Rule-based"]

    # Select difficulty level before the game starts
    difficulty = select_difficulty(screen)
    board = generate_board(difficulty)  # Pass the selected difficulty to the board generation function

    selected = None
    selected_number = None
    running = True

    while running:
        screen.fill((0, 0, 0))
        draw_grid(board, selected)
        draw_number_buttons(selected_number)
        draw_algorithm_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Handle 'n' key press to restart the puzzle
                    board = generate_board(difficulty)  # Regenerate a new board with the same difficulty
                    selected = None
                    selected_number = None
                    display_message(screen, "New puzzle generated", duration=500)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_SIZE and pos[1] < GRID_SIZE:
                    selected = (pos[1] // BLOCK_SIZE, pos[0] // BLOCK_SIZE)
                    if selected_number and board[selected[0]][selected[1]] == 0:
                        if is_valid(board, selected_number, selected[0], selected[1]):
                            board[selected[0]][selected[1]] = selected_number
                elif pos[0] > GRID_SIZE and pos[1] < SCREEN_HEIGHT - BUTTON_AREA_HEIGHT:
                    number_idx = (pos[1] - 10) // (BUTTON_HEIGHT + 10)
                    if 0 <= number_idx < 9:
                        selected_number = number_idx + 1
                elif SCREEN_HEIGHT - BUTTON_AREA_HEIGHT <= pos[1] <= SCREEN_HEIGHT:
                    button_idx = (pos[0] - ((SCREEN_WIDTH - (3 * BUTTON_WIDTH + 2 * BUTTON_GAP)) // 2)) // (
                            BUTTON_WIDTH + BUTTON_GAP)
                    if 0 <= button_idx < len(algo_buttons):
                        algo_func = [solve_with_backtracking, solve_with_constraint_propagation, solve_with_rule_based][
                            button_idx]
                        result = algo_func(board)
                        message = "Puzzle Solved!" if result else "No changes made."
                        display_message(screen, message, duration=500)

        pygame.display.update()


if __name__ == "__main__":
    main()
