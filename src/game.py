import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE, LIGHT_BEIGE
from .gameboard import Gameboard
import math


class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        self.selected_piece = None
        self.gameboard = Gameboard()
        self.turn = WHITE
        self.valid_moves = {}

    def update(self):
        self.gameboard.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected_piece:
            result = self._move(row, col)
            if not result:
                self.selected_piece = None
                self.select(row, col)
                
        piece = self.gameboard.get_piece(row, col)

        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.gameboard.get_valid_moves(piece)
            return True
        
        return False
    
    def _move(self, row, col):
        piece = self.gameboard.get_piece(row, col)
        if self.selected_piece and piece == 0 and (row, col) in self.valid_moves:
            self.gameboard.move(self.selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.gameboard.remove(skipped)
            self.change_turn()                  
        else:
            return False
        
        return True
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            radius = 15

            # Calculate pulsating effect (as in the previous example)
            pulsate_factor = math.sin(pygame.time.get_ticks() * 0.005)
            pulsate_radius = int(radius + radius * 0.1 * pulsate_factor)

            pygame.draw.circle(self.window, LIGHT_BEIGE, center, pulsate_radius)

    def winner(self):
        return self.gameboard.winner()