import pygame
from .constants import DARK, LIGHT, BLACK, WHITE, BLUE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Gameboard:
    def __init__(self):
        self.gameboard = []
        self.selected_piece = None
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()


    def draw_squares(self, win):
        win.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.gameboard.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.gameboard[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.gameboard[row].append(Piece(row, col, WHITE))
                    else:
                        self.gameboard[row].append(0)
                else:
                    self.gameboard[row].append(0)

    def move(self, piece, row, col):
        self.gameboard[piece.row][piece.col], self.gameboard[row][col] = self.gameboard[row][col], self.gameboard[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row, col):
        return self.gameboard[row][col]


    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.gameboard[row][col]
                if piece != 0:
                    piece.draw_piece(win)