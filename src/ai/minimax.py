import pygame
from copy import deepcopy
from ..core.constants import BLACK,WHITE
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("src/sounds/jump_sound.wav")

def minimax(position, depth, max_player, game):
    """
    Returns the best move and its evaluation for a given position, depth, and player using the minimax algorithm.

    Parameters:
    position (Board): The current board state.
    depth (int): The depth of the search tree.
    max_player (bool): True if the player is maximizing, False if minimizing.
    game (Game): The game object.

    Returns:
    (int, Board): A tuple of the evaluation and the best move for the position.
    """
    # Base case: the game is over or the depth limit is reached
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    # Recursive case: explore the possible moves
    if max_player:
        # Initialize the best value and move to the lowest possible
        maxEval = float('-inf')
        best_move = None
        # Loop through all the possible moves for the AI
        for move in get_all_moves(position, BLACK, game):
            # Recursively call minimax on the resulting position, switching the player and decreasing the depth
            evaluation = minimax(move, depth-1, False, game)[0]
            # Update the best value and move if the current evaluation is higher
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        # Return the best value and move for the AI
        return maxEval, best_move
    else:
        # Initialize the best value and move to the highest possible
        minEval = float('inf')
        best_move = None
        # Loop through all the possible moves for the human
        for move in get_all_moves(position, WHITE, game):
            # Recursively call minimax on the resulting position, switching the player and decreasing the depth
            evaluation = minimax(move, depth-1, True, game)[0]
            # Update the best value and move if the current evaluation is lower
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        # Return the best value and move for the human
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    """
    Simulates a move on a board and returns the resulting board.

    Parameters:
    piece (Piece): The piece to move.
    move (tuple): The coordinates of the destination square.
    board (Board): The board to move on.
    game (Game): The game object.
    skip (Piece or None): The piece to skip over if any.

    Returns:
    Board: The board after the move is made.
    """
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    """
    Returns a list of all possible moves for a given board, color, and game.

    Parameters:
    board (Board): The board to get moves from.
    color (int): The color of the pieces to move.
    game (Game): The game object.

    Returns:
    list: A list of boards representing the possible moves.
    """
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

