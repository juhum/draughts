import pygame
from .constants import DARK, LIGHT, BLACK, WHITE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Gameboard:
    """
    A class that represents the board state and logic of a draughts game.

    Attributes:
    gameboard (list): A 2D list of Piece objects or 0s that store the positions of the pieces on the board.
    black_left (int): The number of black pieces left on the board.
    white_left (int): The number of white pieces left on the board.
    black_kings (int): The number of black kings on the board.
    white_kings (int): The number of white kings on the board.
    """
    def __init__(self):
        """
        Initializes the gameboard object by creating an empty 2D list and filling it with Piece objects or 0s according to the initial setup of a draughts game. Also sets the attributes for the number of pieces and kings for each color.
        """
        self.gameboard = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()


    def draw_squares(self, window):
        """
        Draws the light and dark squares on the window to create the board.

        Parameters:
        window (pygame.Surface): The window to draw the squares on.
        """
        window.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        """
        Fills the gameboard list with Piece objects or 0s according to the initial setup of a draughts game. There are 12 pieces of each color.
        """
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
        """
        Moves a piece on the board to a new row and column, and updates the gameboard list accordingly. Also checks if the piece becomes a king by reaching the opposite end of the board, and updates the number of kings for that color.

        Parameters:
        piece (Piece): The piece to move.
        row (int): The new row index of the piece on the board.
        col (int): The new column index of the piece on the board.
        """
        self.gameboard[piece.row][piece.col], self.gameboard[row][col] = self.gameboard[row][col], self.gameboard[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE and not piece.is_king():
                self.white_kings += 1
            elif piece.color == BLACK and not piece.is_king():
                self.black_kings += 1


    def get_piece(self, row, col):
        """
        Returns the piece or 0 at the given row and column on the board.

        Parameters:
        row (int): The row index of the board square.
        col (int): The column index of the board square.

        Returns:
        Piece or 0: The piece or 0 at the given row and column on the board.
        """
        return self.gameboard[row][col]


    def draw(self, window):
        """
        Draws the board and the pieces on the window.

        Parameters:
        window (pygame.Surface): The window to draw the board and the pieces on.
        """
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.gameboard[row][col]
                if piece != 0:
                    piece.draw_piece(window)

    def get_valid_moves(self, piece):
        """
        Returns a dictionary of valid moves for a given piece on the board. The keys are the coordinates of the destination squares, and the values are the lists of 
        pieces that can be skipped by making that move. A move is valid if it is diagonal, within the board boundaries, and either empty or occupied by an enemy 
        piece that can be skipped.

        Parameters:
        piece (Piece): The piece to get the valid moves for.

        Returns:
        dict: A dictionary of valid moves for the piece.
        """
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

        return moves
    

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        Traverses the board diagonally to the left from a given start row and column, and returns a dictionary of valid moves along that direction. The traversal stops when it reaches the stop row, the left edge of the board, or a friendly piece. If an enemy piece is encountered, it can be skipped if the next square is empty, and the traversal continues with the skipped piece added to the list of skipped pieces.

        Parameters:
        start (int): The start row index of the traversal.
        stop (int): The stop row index of the traversal.
        step (int): The step size of the traversal (-1 for up, 1 for down).
        color (int): The color of the piece that is moving (WHITE or BLACK).
        left (int): The start column index of the traversal.
        skipped (list): The list of pieces that have been skipped so far. Default is an empty list.

        Returns:
        dict: A dictionary of valid moves along the left diagonal direction.
        """
        moves = {}
        last = []
        # Loop through the rows from start to stop with the given step
        for row_ in range(start, stop, step):
            # If the column index is out of bounds, break the loop
            if left < 0:
                break
            
            # Get the piece or 0 at the current row and column
            current = self.gameboard[row_][left]
            # If the current square is empty
            if current == 0:
                if skipped and not last: # If there are skipped pieces but no last piece, break the loop
                    break
                elif skipped: # If there are skipped pieces and a last piece
                    moves[(row_, left)] = last + skipped # Add the move to the dictionary with the last and skipped pieces as the value
                else: # If there are no skipped pieces
                    moves[(row_, left)] = last # Add the move to the dictionary with the last piece as the value
                
                if last: # If there is a last piece
                    if step == -1: # If the step is -1 (moving up)
                        row = max(row_ - 3, -1) # Set the stop row to the maximum of the current row minus 3 and -1
                    else: # If the step is 1 (moving down)
                        row = min(row_ + 3, ROWS) # Set the stop row to the minimum of the current row plus 3 and the number of rows

                    if skipped: # If there are skipped pieces recursively traverse left and right from the next row with the last and skipped pieces as the skipped list
                        moves.update(self._traverse_left(row_ + step, row, step, color, left - 1, skipped=last+skipped))
                        moves.update(self._traverse_right(row_ + step, row, step, color, left + 1, skipped=last+skipped))
                    else: # If there are no skipped pieces recursively traverse left and right from the next row with the last piece as the skipped list
                        moves.update(self._traverse_left(row_ + step, row, step, color, left - 1, skipped=last))
                        moves.update(self._traverse_right(row_ + step, row, step, color, left + 1, skipped=last))

                break # Break the loop after adding the move
            elif current.color == color: # If the current square is occupied by a friendly piece, break the loop
                break
            else: # If the current square is occupied by an enemy piece
                last = [current] # Set the last piece to the current piece

            left -= 1 # Decrease the column index by 1

        return moves # Return the dictionary of valid moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """
        Traverses the board diagonally to the right from a given start row and column, and returns a dictionary of valid moves along that direction. The traversal stops when it reaches the stop row, the right edge of the board, or a friendly piece. If an enemy piece is encountered, it can be skipped if the next square is empty, and the traversal continues with the skipped piece added to the list of skipped pieces.

        Parameters:
        start (int): The start row index of the traversal.
        stop (int): The stop row index of the traversal.
        step (int): The step size of the traversal (-1 for up, 1 for down).
        color (int): The color of the piece that is moving (WHITE or BLACK).
        right (int): The start column index of the traversal.
        skipped (list): The list of pieces that have been skipped so far. Default is an empty list.

        Returns:
        dict: A dictionary of valid moves along the right diagonal direction.
        """
        moves = {}
        last = []
        for row_ in range(start, stop, step): # Loop through the rows from start to stop with the given step
            if right >= COLS: # If the column index is out of bounds, break the loop
                break
            current = self.gameboard[row_][right] # Get the piece or 0 at the current row and column
            if current == 0: # If the current square is empty
                if skipped and not last:  # If there are skipped pieces but no last piece, break the loop
                    break
                elif skipped: # If there are skipped pieces and a last piece
                    moves[(row_, right)] = last + skipped # Add the move to the dictionary with the last and skipped pieces as the value
                else: # If there are no skipped pieces
                    moves[(row_, right)] = last # Add the move to the dictionary with the last piece as the value
                if last: # If there is a last piece
                    if step == -1: # If the step is -1 (moving up)
                        row = max(row_ - 3, -1) # Set the stop row to the maximum of the current row minus 3 and -1
                    else: # If the step is 1 (moving down)
                        row = min(row_ + 3, ROWS) # Set the stop row to the minimum of the current row plus 3 and the number of rows

                    if skipped: # If there are skipped pieces recursively traverse left and right from the next row with the last and skipped pieces as the skipped list
                        moves.update(self._traverse_left(row_ + step, row, step, color, right - 1, skipped=last+skipped))
                        moves.update(self._traverse_right(row_ + step, row, step, color, right + 1, skipped=last+skipped))
                    else: # If there are no skipped pieces recursively traverse left and right from the next row with the last piece as the skipped list
                        moves.update(self._traverse_left(row_ + step, row, step, color, right - 1, skipped=last))
                        moves.update(self._traverse_right(row_ + step, row, step, color, right + 1, skipped=last))

                break # Break the loop after adding the move
            elif current.color == color: # If the current square is occupied by a friendly piece, break the loop
                break
            else: # If the current square is occupied by an enemy piece
                last = [current] # Set the last piece to the current piece
                
            right += 1 # Increase the column index by 1
        
        return moves # Return the dictionary of valid moves
    

    def remove(self, pieces):
        """
        Removes a list of pieces from the board and updates the gameboard list and the number of pieces left for each color.

        Parameters:
        pieces (list): A list of Piece objects to remove from the board.
        """
        for piece in pieces:
            self.gameboard[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        """
        Returns the winner of the game, or None if there is no winner yet. The winner is the color that has no pieces left on the board.

        Returns:
        str or None: The winner of the game, or None if there is no winner yet.
        """
        if self.black_left <= 0:
            return 'WHITE'
        elif self.white_left <= 0:
            return 'BLACK'
        
        return None
    
    def evaluate(self):
        """
        Returns a numerical evaluation of the board state for the minimax algorithm. The evaluation is the difference between the number of black pieces and white pieces, plus a small bonus for each king.

        Returns:
        int: The evaluation of the board state.
        """
        return self.black_left - self.white_left + (self.black_kings * 0.5 - self.white_kings * 0.5)

    
    def get_all_pieces(self, color):
        """
        Returns a list of all the pieces on the board that have the given color.

        Parameters:
        color (int): The color of the pieces to get (WHITE or BLACK).

        Returns:
        list: A list of Piece objects that have the given color.
        """
        pieces = []
        for row in self.gameboard:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    