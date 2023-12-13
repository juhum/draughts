import pygame
from copy import deepcopy

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# ai moving only diagonally, king stuck in corner
def minimax(postion, depth, max_player, game):
    if depth == 0 or postion.winner != None:
        return postion.evaluate(), postion

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(postion, BLACK, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(postion, WHITE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move
    
def get_all_moves(gameboard, color, game):
    moves = []
    for piece in gameboard.get_all_pieces(color):
        valid_moves = gameboard.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(gameboard)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves


def simulate_move(piece, move, board, game, skip):
    board.move_piece_to(piece, move[0], move[1])
    if skip:
        for coord in skip:
            skip_piece = board.get_piece(coord[0], coord[1])
            board.capture_piece(skip_piece)
    return board

# def draw_moves(game, board, piece):
#     valid_moves = board.get_valid_moves(piece)
#     board.draw(game.window)
#     pygame.draw.circle(game.window, (0, 255, 0), (piece.x, piece.y), 50, 5)
#     game.draw_valid_moves(valid_moves.keys())
#     pygame.display.update()
#     #pygame.time.delay(100)
