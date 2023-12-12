import pygame
from src.constants import WIDTH, HEIGHT, SQUARE_SIZE
from src.gameboard import Gameboard
from src.game import Game

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

        
        game.update()
        

    pygame.quit()

main()