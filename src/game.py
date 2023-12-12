import pygame
from .constants import BLACK, WHITE
from .gameboard import Gameboard

class Game:
    def __init__(self, window):
        self.window = window
        self.gameboard = Gameboard()
        self.selected_piece = None
        # self.black_left = self._white_left = 12
        # self.black_kings = self._white_kings = 0
        self.turn = WHITE
        self.valid_moves = {}

    def update(self):
        self.gameboard.draw(self.window)
        #self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self.__init__(self.window) # test this

    def select(self, row, col):
        if self.selected_piece:
            result = self._move(row, col)
            if not result:
                self.selected_piece = None
                self.select(row, col)
        else:
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
          #  skipped = self.valid_moves[(row, col)]
           # if skipped:                         # to test
           #     self.gameboard.remove(skipped)  #to test
            self.change_turn()                  #to test
        else:
            return False
        
        return True
    
    def change_turn(self):
        #self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_valid_moves(self, moves):
        