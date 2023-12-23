import pygame
from copy import deepcopy

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# ai moving only diagonally, king stuck in corner
def minimax(postion, depth, max_player, game):
    if depth == 0 or postion.winner != None:
        print("Depth is 0 or there is a winner.")
        return postion.evaluate(), postion

    if max_player:
        print("Max player's turn.")
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(postion, BLACK, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    else:
        print("Min player's turn.")
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(postion, WHITE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        print("Evaluated Move:", best_move)
        return min_eval, best_move
    
def get_all_moves(gameboard, color, game):
    moves = []
    print("getting moves")

    for piece in gameboard.get_all_pieces(color):
        valid_moves = gameboard.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(gameboard)

            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


def simulate_move(piece, move, gameboard, game, skip):
    gameboard.move(piece, move[0], move[1])
    if skip:
        gameboard.remove(skip)

    return gameboard


