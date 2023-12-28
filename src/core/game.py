import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE, LIGHT_BEIGE
from .gameboard import Gameboard
import math
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("src/sounds/jump_sound.wav")

class Game:
    """
    A class that represents the game logic and state of a draughts game.
    
    Attributes:
    window (pygame.Surface): The window to display the game on.
    selected_piece (Piece or None): The piece that is currently selected by the user, or None if no piece is selected.
    gameboard (Gameboard): The gameboard object that stores the pieces and their positions.
    turn (int): The color of the player whose turn it is (WHITE or BLACK).
    valid_moves (dict): A dictionary that maps the coordinates of the valid moves to the pieces that can be skipped by making that move.
    winner_moves (str or None): The winner of the game, or None if there is no winner yet.
    """
    def __init__(self, window):
        """
        Initializes the game object with a window and calls the _init method to set up the game state.
        """
        self._init()
        self.window = window

    def _init(self):
        """
        Sets up the initial game state by creating a gameboard, setting the turn to WHITE, and clearing the selected piece and the valid moves.
        """
        self.selected_piece = None
        self.gameboard = Gameboard()
        self.turn = WHITE
        self.valid_moves = {}
        self.winner_moves = None

        

    def update(self):
        """
        Updates the game display by drawing the gameboard and the valid moves on the window.
        """
        self.gameboard.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        """
        Resets the game state by calling the _init method.
        """
        self._init()

    def select(self, row, col):
        """
        Selects a piece on the board if it belongs to the current player and has valid moves, or tries to move the selected piece to the given row and column.

        Parameters:
        row (int): The row index of the board square to select or move to.
        col (int): The column index of the board square to select or move to.

        Returns:
        bool: True if the selection or move was successful, False otherwise.
        """
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
        """
        Firstly checks if there any valid moves for every piece, if not the winner is opposite color.
        Then tries to move the selected piece to the given row and column, and removes any skipped pieces. 
        If the move is valid, changes the turn and clears the selected piece and the valid moves.

        Parameters:
        row (int): The row index of the destination square.
        col (int): The column index of the destination square.

        Returns:
        winner_moves: opposite color if current player does not have any valid moves
        bool: True if the move was successful, False otherwise.
        """
        remaining_pieces = self.gameboard.get_all_pieces(self.turn)
        any_valid_moves = False # initialize a variable to store if there are any valid moves
        for piece in remaining_pieces:
            valid_moves = self.gameboard.get_valid_moves(piece) # use a different variable name than valid_moves_pieces
            if valid_moves:
                print(f"{self.turn} piece at ({piece.row}, {piece.col}) has valid moves: {valid_moves}")
                any_valid_moves = True # set the variable to True if there is at least one valid move

        if not any_valid_moves: # use the variable to check if there are no valid moves
            self.winner_moves = 'WHITE' if self.turn == BLACK else 'BLACK'         
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
        """
        Changes the turn to the opposite color and clears the valid moves.
        """
        self.valid_moves = {} 
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        print("Turn changed:", self.turn)



    def draw_valid_moves(self, moves):
        """
        Draws circles on the board squares that represent the valid moves for the selected piece.

        Parameters:
        moves (dict): A dictionary that maps the coordinates of the valid moves to the pieces that can be skipped by making that move.
        """
        for move in moves:
            row, col = move
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            radius = 15

            # Calculate pulsating effect
            pulsate_factor = math.sin(pygame.time.get_ticks() * 0.005)
            pulsate_radius = int(radius + radius * 0.1 * pulsate_factor)

            pygame.draw.circle(self.window, LIGHT_BEIGE, center, pulsate_radius)

    def winner(self):
        """
        Returns the winner of the game, or None if there is no winner yet.

        Returns:
        str or None: The winner of the game, or None if there is no winner yet.
        """
        if self.winner_moves is not None:
            return self.winner_moves
        
        return self.gameboard.winner()
    

    def ai_move(self, gameboard):
        """
        Makes a move for the AI by updating the gameboard, changing the turn, and playing a sound.

        Parameters:
        gameboard (Gameboard): The gameboard object that represents the AI's move.
        """
        self.gameboard = gameboard
        self.change_turn()
        jump_sound.play()


    def get_board(self):
        """
        Returns the gameboard object.

        Returns:
        Gameboard: The gameboard object that stores the pieces and their positions.
        """
        return self.gameboard