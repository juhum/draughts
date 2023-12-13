import pygame
from src.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from src.gameboard import Gameboard
from src.game import Game
from src.ai import minimax

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Draughts')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    while run:
        clock.tick(FPS)

        if game.turn == BLACK:
            value, new_board = minimax(game.gameboard, 3, BLACK, game)
            game.ai_move(new_board)


        if game.winner() != None:
            print("winner" + str(game.winner()))
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