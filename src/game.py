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
        self.turn = WHITE
        self.valid_moves_of_selected_piece = {}
        self.gameboard = Gameboard()

    def update(self):
        self.gameboard.draw(self.window)
        self._draw_valid_moves(self.valid_moves_of_selected_piece)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col) -> bool:
        if self.selected_piece:
            # try moving the piece to the new location
            successful_move = self._move(row, col)
            if successful_move:
                self.selected_piece = None
                self.valid_moves_of_selected_piece = {}
                return False
            else:
                # if not successful, deselect the current piece. Try to select the piece in the new location instead if possible
                self.selected_piece = None
                return self.select(row, col)
        else:
            # try to select the piece under the mouse
            piece = self.gameboard.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                # the square under the cursor has a piece of the player's color: select it
                self.selected_piece = piece
                self.valid_moves_of_selected_piece = self.gameboard.get_valid_moves(piece)
                #print(f"location: ({row}, {col})")
                #print(f"valid moves: {self.valid_moves}")
                return True
            else:
                return False
    
    def _move(self, row, col) -> bool:
        # move the piece that is selected
        target = self.gameboard.get_piece(row, col)
        if target == 0 and (row, col) in self.valid_moves_of_selected_piece:
            self.gameboard.move_piece_to(self.selected_piece, row, col)
            for enemy_piece_loc in self.valid_moves_of_selected_piece[(row, col)]:
                row, col = enemy_piece_loc
                enemy_piece = self.gameboard.get_piece(row, col)
                self.gameboard.capture_piece(enemy_piece)
            self._change_turn()
            return True
        else:
            return False
    
    def _change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        self.update()
        if not self.gameboard.has_valid_moves(self.turn):
            self.gameboard.winner = 1 - self.gameboard.color_to_player_map[self.turn]

    def _draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            radius = 15

            # Calculate pulsating effect (as in the previous example)
            pulsate_factor = math.sin(pygame.time.get_ticks() * 0.005)
            pulsate_radius = int(radius + radius * 0.1 * pulsate_factor)

            pygame.draw.circle(self.window, LIGHT_BEIGE, center, pulsate_radius)

    def winner(self):
        return self.gameboard.winner
    
    def get_board(self):
        return self.gameboard
    
    def get_all_pieces(self, color):
        return self.pieces[self.color_to_player_map[color]]
    
    def ai_move(self, gameboard):
        self.gameboard = gameboard
        self._change_turn()