import pygame
from pygame.locals import *
from src.core.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from src.core.game import Game
from src.ai import minimax

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False
winner = None
pygame.display.set_caption('Draughts')
pygame.init()

def get_row_col_from_mouse(pos):
    """
    Returns the row and column indices of the board square corresponding to the mouse position.

    Parameters:
    pos (tuple): The x and y coordinates of the mouse position.

    Returns:
    (int, int): A tuple of the row and column indices.
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def show_menu(window, game_over=False, winner=None):
    """
    Displays a menu screen with two options: start game or quit.

    Parameters:
    window (pygame.Surface): The window to display the menu on.
    game_over (bool): True if the game is over, False otherwise. Default is False.
    winner (str or None): The winner of the game, or None if there is no winner. Default is None.

    Returns:
    int: The index of the chosen option (1 for start game, 2 for quit).
    """
    pygame.init()
    menu_font = pygame.font.Font(None, 36)
    menu_text = ["Start Game", "Quit"]
    menu_buttons = [menu_font.render(text, True, WHITE) for text in menu_text]
    button_rects = [button.get_rect(center=(WIDTH // 2, i * 100 + HEIGHT // 2)) for i, button in enumerate(menu_buttons)]
    button_colors = [BLACK, BLACK]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        return i + 1  # Return the button index (1-indexed)
                    
        
        game = Game(WINDOW)
        game.gameboard.draw_squares(window)
        for button, rect, color in zip(menu_buttons, button_rects, button_colors):
            pygame.draw.rect(window, color, rect.inflate(10, 10))  # Draw colored button background
            window.blit(button, rect)  # Draw button text

        if game_over and winner is not None:
            winner_text = f"Winner: {winner}"
            # Render text with white color
            winner_font = pygame.font.Font(None, 48)
            winner_surface = winner_font.render(winner_text, True, WHITE)
            winner_rect = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

            # Render text with black outline
            outline_font = pygame.font.Font(None, 48)
            outline_surface = outline_font.render(winner_text, True, BLACK)
            outline_rect = outline_surface.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 - 98))  # Slightly offset for the outline effect

            # Blit the outline first and then the text on top
            window.blit(outline_surface, outline_rect)
            window.blit(winner_surface, winner_rect)

        pygame.display.flip()



def run_game():
    """
    Runs the main game loop until the game ends or the user quits.

    Returns:
    str or None: The winner of the game, or None if the game doesn't end.
    """
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    global game_over
    global winner 
    
    while run:
        clock.tick(FPS)

        if game.turn == BLACK:
            value, new_board = minimax(game.get_board(), 4, True, game)
            game.ai_move(new_board)

        if game.winner() is not None:
            winner = game.winner()
            game_over = True
            return winner  # Return the winner when the game ends

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    return None  # Return None when the game doesn't end

def main():
    """
    The main function that initializes the pygame window and runs the game menu.
    """
    global winner
    global game_over
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Draughts')

    while True:
        choice = show_menu(window, game_over, winner)

        if choice == 1:
            winner = run_game()
            if winner is not None:
                game_over = True
            else:
                game_over = False
                winner = None
        elif choice == 2:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

    pygame.quit()



main()