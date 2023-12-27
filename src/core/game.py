import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE, LIGHT_BEIGE
from .gameboard import Gameboard
import math
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("src/sounds/jump_sound.wav")

class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        self.selected_piece = None
        self.gameboard = Gameboard()
        self.turn = WHITE
        self.valid_moves = {}
        self.winner_moves = None

        

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
        remaining_pieces = self.gameboard.get_all_pieces(self.turn)
        any_valid_moves = False # initialize a variable to store if there are any valid moves
        for piece in remaining_pieces:
            valid_moves = self.gameboard.get_valid_moves(piece) # use a different variable name than valid_moves_pieces
            if valid_moves:
                print(f"{self.turn} piece at ({piece.row}, {piece.col}) has valid moves: {valid_moves}")
                any_valid_moves = True # set the variable to True if there is at least one valid move

        if not any_valid_moves: # use the variable to check if there are no valid moves
            self.winner_moves = 'WHITE' if self.turn == BLACK else 'BLACK'          # WINNER IS NOT METHOD FOR SETTING WINNER, IT JUST CALCULATES DEPENDING IF THERE ARE 0, NEED TO SET VARIABLE 
            print("No valid moves for any pieces. Game over.")

        piece = self.gameboard.get_piece(row, col)
        if self.selected_piece and piece == 0 and (row, col) in self.valid_moves:
            self.gameboard.move(self.selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.gameboard.remove(skipped)
            self.change_turn()                  
        else:
            return False
        jump_sound.play()
        return True
    
    def change_turn(self):
        self.valid_moves = {} # remove this line or use it to store the valid moves for each piece
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        print("Turn changed:", self.turn)



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
        if self.winner_moves is not None:
            return self.winner_moves
        
        return self.gameboard.winner()
    

    def ai_move(self, gameboard):
        self.gameboard = gameboard
        self.change_turn()
        jump_sound.play()


    def get_board(self):
        return self.gameboard