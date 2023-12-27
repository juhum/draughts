import pygame
from .constants import BLACK, WHITE, SQUARE_SIZE, YELLOW, GRAY, GRAY_LIGHT
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
class Piece:
    PADDING = 20
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        if not self.is_king():
            self.king = True

    def is_king(self) -> bool:
        return self.king

    def draw_piece(self, window):
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
        self.row = row
        self.col = col
        self.calculate_position()
        
    
    def __repr__(self):
        return str(self.color)