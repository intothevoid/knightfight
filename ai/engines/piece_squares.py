import chess
import chess.polyglot
from ai.engines.piece_tables import (
    pawntable,
    knightstable,
    bishopstable,
    rookstable,
    queenstable,
    kingstable,
)

"""
See piece_squares2.py for an improved version of this technique.

https://andreasstckl.medium.com/writing-a-chess-program-in-one-day-30daff4610ec
https://www.chessprogramming.org/Simplified_Evaluation_Function

Piece-square tables

I used the piece-square tables from https://www.chessprogramming.org/Simplified_Evaluation_Function

For each sort of piece, a different table is defined. If the value on a square is positive then the 
program tries to place a piece on that square if the value is negative it avoids to move to that square. 
The value of the whole position is calculated by summing over all pieces of both sides.

For pawns, the program is encouraged to advance the pawns. Additionally, we try to discourage the engine 
from leaving central pawns unmoved. Pawns on f2, g2 or c2 and b2 should not move tof3, etc.

Knights are simply encouraged to go to the center. Standing on the edge is a bad idea.

Bishops should avoid corners and borders.

Rooks should occupy the 7th rank and avoid a, h columns

Queens should avoid corners and borders and stay in the center.

Kings should stand behind the pawn shelter. This is only good for the opening and middle game phase. 

The endgame needs a different table. I will do this in a future enhancement of the program.
"""


movehistory = []


def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = (
        100 * (wp - bp)
        + 320 * (wn - bn)
        + 330 * (wb - bb)
        + 500 * (wr - br)
        + 900 * (wq - bq)
    )

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum(
        [
            -pawntable[chess.square_mirror(i)]
            for i in board.pieces(chess.PAWN, chess.BLACK)
        ]
    )
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum(
        [
            -knightstable[chess.square_mirror(i)]
            for i in board.pieces(chess.KNIGHT, chess.BLACK)
        ]
    )
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum(
        [
            -bishopstable[chess.square_mirror(i)]
            for i in board.pieces(chess.BISHOP, chess.BLACK)
        ]
    )
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum(
        [
            -rookstable[chess.square_mirror(i)]
            for i in board.pieces(chess.ROOK, chess.BLACK)
        ]
    )
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum(
        [
            -queenstable[chess.square_mirror(i)]
            for i in board.pieces(chess.QUEEN, chess.BLACK)
        ]
    )
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum(
        [
            -kingstable[chess.square_mirror(i)]
            for i in board.pieces(chess.KING, chess.BLACK)
        ]
    )

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval


def alphabeta(alpha, beta, depthleft, board):
    bestscore = -9999
    if depthleft == 0:
        return quiesce(alpha, beta, board)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1, board)
        board.pop()
        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
        if score > alpha:
            alpha = score
    return bestscore


def quiesce(alpha, beta, board):
    stand_pat = evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha, board)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def get_informed_move(board: chess.Board, depth: int):
    try:
        move = (
            chess.polyglot.MemoryMappedReader("bookfish.bin")
            .weighted_choice(board)
            .move
        )
        movehistory.append(move)
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1, board)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            board.pop()
        movehistory.append(bestMove)
        return bestMove
