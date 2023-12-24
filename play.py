import pygame
from pygame.locals import *
from src.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from src.game import Game
from src.ai import minimax

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Draughts')
# sounds fix, better menu, after winning/losing screen, no possible moves for any piece = lose 
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def show_menu(window):
    menu_font = pygame.font.Font(None, 36)
    menu_text = ["Start New Game", "Quit"]
    menu_buttons = [menu_font.render(text, True, WHITE) for text in menu_text]
    button_rects = [button.get_rect(center=(WIDTH // 2, i * 100 + HEIGHT // 2)) for i, button in enumerate(menu_buttons)]

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

        window.fill(BLACK)
        for button, rect in zip(menu_buttons, button_rects):
            window.blit(button, rect)

        pygame.display.flip()



def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Draughts')

    while True:
        choice = show_menu(window)

        if choice == 1:
            run_game()
        elif choice == 2:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")




def run_game():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    
    while run:
        clock.tick(FPS)

        if game.turn == BLACK:
            value, new_board = minimax(game.get_board(), 4, True, game)
            print("AI Decision:", value, new_board)
            game.ai_move(new_board)
            print("AI moved")



        if game.winner() != None:
             print(game.winner())
             run = False
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        
        game.update()
        

    pygame.quit()

main()