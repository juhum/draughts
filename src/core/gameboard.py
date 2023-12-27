import pygame
from .constants import DARK, LIGHT, BLACK, WHITE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("src/sounds/jump_sound.wav")

class Gameboard:
    def __init__(self):
        self.gameboard = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()


    def draw_squares(self, window):
        window.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
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
            if piece.color == WHITE and not piece.is_king():
                self.white_kings += 1
            elif piece.color == BLACK and not piece.is_king():
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

        return moves
    

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for row_ in range(start, stop, step):
            if left < 0:
                break

            current = self.gameboard[row_][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row_, left)] = last + skipped
                else:
                    moves[(row_, left)] = last
                
                if last:
                    if step == -1:
                        row = max(row_ - 3, -1)
                    else:
                        row = min(row_ + 3, ROWS)

                    if skipped:
                        moves.update(self._traverse_left(row_ + step, row, step, color, left - 1, skipped=last+skipped))
                        moves.update(self._traverse_right(row_ + step, row, step, color, left + 1, skipped=last+skipped))
                    else:
                        moves.update(self._traverse_left(row_ + step, row, step, color, left - 1, skipped=last))
                        moves.update(self._traverse_right(row_ + step, row, step, color, left + 1, skipped=last))

                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for row_ in range(start, stop, step):
            if right >= COLS:
                break
            current = self.gameboard[row_][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row_, right)] = last + skipped
                else:
                    moves[(row_, right)] = last
                if last:
                    if step == -1:
                        row = max(row_ - 3, -1)
                    else:
                        row = min(row_ + 3, ROWS)

                    if skipped:
                        moves.update(self._traverse_left(row_ + step, row, step, color, right - 1, skipped=last+skipped))
                        moves.update(self._traverse_right(row_ + step, row, step, color, right + 1, skipped=last+skipped))
                    else:
                        moves.update(self._traverse_left(row_ + step, row, step, color, right - 1, skipped=last))
                        moves.update(self._traverse_right(row_ + step, row, step, color, right + 1, skipped=last))

                break
            elif current.color == color:
                break
            else:
                last = [current]
                
            right += 1
        
        return moves
    

    def remove(self, pieces):
        for piece in pieces:
            self.gameboard[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        if self.black_left <= 0:
            return 'WHITE'
        elif self.white_left <= 0:
            return 'BLACK'
        
        return None
    
    def evaluate(self):
        return self.black_left - self.white_left + (self.black_kings * 0.5 - self.white_kings * 0.5)

    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.gameboard:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    