import pygame
from .constants import DARK, LIGHT, BLACK, WHITE, BLUE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
make_king_sound = pygame.mixer.Sound("sounds/make_king_sound.wav")

class Gameboard:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.winner = None      # 0/1 if 1/0 has 0 pieces
        self.color_to_player_map = {
            WHITE: 0, 
            BLACK: 1,
            }
        self.number_pieces_player_1_2 = [0, 0]
        self.number_kings_player_1_2 = [0, 0]
        self.pieces = [[], []]  # a list with the individual pieces
        self.create_board()


    def _draw_background(self, window):
        window.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    
    def _add_new_piece(self, row, col, player_color):
        new_piece = Piece(row, col, player_color)
        player_index = self.color_to_player_map[player_color]
        self.pieces[player_index].append(new_piece)
        self.board[row].append(new_piece)
        self.number_pieces_player_1_2[player_index] += 1

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 != row % 2:
                    if row < 3:
                        self._add_new_piece(row, col, BLACK)
                    elif row > 4:
                        self._add_new_piece(row, col, WHITE)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move_piece_to(self, piece, row, col):
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col]
        piece.move_to(row, col)

        # no further checks needed, because of direction limitations
        if (row == 0 or row == ROWS - 1) and not piece.is_king():
            piece.make_king()
            self.number_kings_player_1_2[self.color_to_player_map[piece.color]] += 1
        jump_sound.play()

    def get_piece(self, row, col):
        return self.board[row][col]
    

    def capture_piece(self, piece):
        owner_index = self.color_to_player_map[piece.color]
        self.pieces[owner_index].remove(piece)
        self.number_pieces_player_1_2[owner_index] -= 1
        if piece.is_king():
            self.number_kings_player_1_2[owner_index] -= 1
        if self.number_pieces_player_1_2[owner_index] == 0:
            self.winner = 1 - owner_index
        self.board[piece.row][piece.col] = 0


    def draw(self, window):
        self._draw_background(window)
        for row in range(ROWS):
            for col in range(COLS):
                field_content = self.board[row][col]
                if field_content != 0:
                    field_content.draw(window)


    def can_jump_from_to(self, piece, old_row, old_col, new_row, new_col, step_size) -> bool:
        '''evaluates to True if boundaries are right and if current piece between start/end location is of different color'''
        if not (piece.is_king() or new_row == old_row + piece.direction * step_size):
            # invalid direction
            return False
        if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
            # outside of board
            return False
        new_loc = self.get_piece(new_row, new_col)
        if new_loc != 0:
            # jump location not empty
            return False
        # all base obstacles have been overcome
        if step_size == 2:
            middle_row = (old_row + new_row) // 2
            middle_col = (old_col + new_col) // 2
            middle_piece = self.get_piece(middle_row, middle_col)
            if middle_piece == 0 or middle_piece.color == piece.color:
                return False
        
        return True

    def _get_valid_moves(self, piece, row, col, jump_path, step_size):
        ''' this method takes in a row and col of where the piece is currently during the jump. It also takes a jump_path so a king
        does not jump back to where it came from and to prevent jumping over the same piece twice.
        Finally a step_size is provided: if it's 1 only short jumps are considered, if 2 then jump chains are considered
        '''
        # incomplete: two different move_paths can have identical end locations
        up, down, left, right = [x + y * step_size for x in [row, col] for y in [-1, +1]]
        moves = {}

        for new_col in [left, right]:
            for new_row in [up, down]:
                if not self.can_jump_from_to(piece, row, col, new_row, new_col, step_size):
                    continue
                
                if step_size == 1:
                    moves[new_row, new_col] = []
                else:
                    middle_row = (new_row + row) // 2
                    middle_col = (new_col + col) // 2
                    if (middle_row, middle_col) in jump_path:
                        continue
                    new_jump_path = jump_path.copy()
                    new_jump_path.append((middle_row, middle_col))
                    moves[(new_row, new_col)] = new_jump_path
                    # recursive call
                    moves.update(self._get_valid_moves(piece, new_row, new_col, new_jump_path, step_size))
        return moves

    def get_valid_moves(self, piece):
        '''
        returns a dictionary with locations as keys and lists of pieces as values.
        '''
        moves = {}  # dictionary with valid final locations as keys and the values are the pieces that got jumped
        moves.update(self._get_valid_moves(piece, piece.row, piece.col, [], 1))
        moves.update(self._get_valid_moves(piece, piece.row, piece.col, [], 2))

        return moves
    

    def has_valid_moves(self, color):
        player_index = self.color_to_player_map[color]
        for piece in self.pieces[player_index]:
            moves = self.get_valid_moves(piece)
            if moves:
                return True
        
        return False

    def evaluate(self):
        '''This calculates the score of the board used by the minimax algorithm'''
        score = 0
        score += 3 * (self.number_pieces_player_1_2[0] - self.number_pieces_player_1_2[1])
        score += 1 * (self.number_kings_player_1_2[0] - self.number_kings_player_1_2[1])

        return  score


    def get_all_pieces(self, color):
        return self.pieces[self.color_to_player_map[color]]
    

