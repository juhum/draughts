import pygame
from .constants import DARK, LIGHT, BLACK, WHITE, BLUE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Gameboard:
    def __init__(self):
        self.gameboard = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()


    def draw_squares(self, window):
        window.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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


    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.gameboard[row][col]
                if piece != 0:
                    piece.draw_piece(window)

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        pass

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        pass