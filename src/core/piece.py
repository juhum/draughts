import pygame
from .constants import BLACK, WHITE, SQUARE_SIZE, YELLOW, GRAY, GRAY_LIGHT

class Piece:
    """
    A class that represents a piece on the draughts board.

    Attributes:
    row (int): The row index of the piece on the board.
    col (int): The column index of the piece on the board.
    color (int): The color of the piece (WHITE or BLACK).
    king (bool): True if the piece is a king, False otherwise.
    x (int): The x coordinate of the center of the piece on the window.
    y (int): The y coordinate of the center of the piece on the window.
    PADDING (int): The padding between the edge of the square and the piece.
    OUTLINE (int): The thickness of the outline around the piece.
    """
    PADDING = 20
    OUTLINE = 2

    def __init__(self, row, col, color):
        """
        Initializes the piece object with a row, a column, and a color, and sets the king attribute to False. Also calls the calculate_position method to set the x and y attributes.
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        """
        Calculates the x and y coordinates of the center of the piece on the window based on the row and column indices and the square size.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """
        Makes the piece a king if it is not already a king.
        """
        if not self.is_king():
            self.king = True

    def is_king(self) -> bool:
        """
        Returns True if the piece is a king, False otherwise.
        """
        return self.king

    def draw_piece(self, window):
        """
        Draws the piece on the window with a shadow, an outline, and a crown if it is a king.

        Parameters:
        window (pygame.Surface): The window to draw the piece on.
        """
        radius = SQUARE_SIZE // 2 - self.PADDING

        # Draw shadow beneath the piece
        shadow_radius = radius + 5
        pygame.draw.circle(window, GRAY, (self.x + 2, self.y + 2), shadow_radius)

        # Draw the piece with an outline
        pygame.draw.circle(window, GRAY_LIGHT, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)

        # Draw a crown if the piece is a king
        if self.king:
            crown_offset = 10
            pygame.draw.polygon(
                window,
                YELLOW,
                [
                    (self.x - crown_offset, self.y - radius - self.OUTLINE),
                    (self.x + crown_offset, self.y - radius - self.OUTLINE),
                    (self.x, self.y - radius - self.OUTLINE - crown_offset),
                ],
            )
    
    def move(self, row, col):
        """
        Moves the piece to a new row and column, and updates the x and y coordinates accordingly.

        Parameters:
        row (int): The new row index of the piece on the board.
        col (int): The new column index of the piece on the board.
        """
        self.row = row
        self.col = col
        self.calculate_position()
        
    
    def __repr__(self):
        """
        Returns a string representation of the piece's color.
        """
        return str(self.color)