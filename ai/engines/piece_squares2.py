"""
Tweaked version of -
https://medium.datadriveninvestor.com/an-incremental-evaluation-function-and-a-testsuite-for-computer-chess-6fde22aac137
"""
from typing import Optional
import chess
import chess.svg
from ai.engines.piece_tables import (
    pawntable,
    knightstable,
    bishopstable,
    rookstable,
    queenstable,
    kingstable,
)

movehistory = []


def init_evaluate_board(board: chess.Board):
    global boardvalue

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

    boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

    return boardvalue


def evaluate_board(board: chess.Board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    eval = boardvalue
    if board.turn:
        return eval
    else:
        return -eval


piecetypes = [
    chess.PAWN,
    chess.KNIGHT,
    chess.BISHOP,
    chess.ROOK,
    chess.QUEEN,
    chess.KING,
]
tables = [pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]
piecevalues = [100, 320, 330, 500, 900]
boardvalue = 0


def update_eval(
    board: chess.Board, mov: chess.Move, side: chess.Color
) -> Optional[chess.Move]:
    global boardvalue

    # update piecequares
    movingpiece = board.piece_type_at(mov.from_square)
    if movingpiece:
        if side:
            boardvalue = boardvalue - tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E1) and (mov.to_square == chess.G1):
                boardvalue = boardvalue - rookstable[chess.H1]
                boardvalue = boardvalue + rookstable[chess.F1]
            elif (mov.from_square == chess.E1) and (mov.to_square == chess.C1):
                boardvalue = boardvalue - rookstable[chess.A1]
                boardvalue = boardvalue + rookstable[chess.D1]
        else:
            boardvalue = boardvalue + tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E8) and (mov.to_square == chess.G8):
                boardvalue = boardvalue + rookstable[chess.H8]
                boardvalue = boardvalue - rookstable[chess.F8]
            elif (mov.from_square == chess.E8) and (mov.to_square == chess.C8):
                boardvalue = boardvalue + rookstable[chess.A8]
                boardvalue = boardvalue - rookstable[chess.D8]

        if side:
            boardvalue = boardvalue + tables[movingpiece - 1][mov.to_square]
        else:
            boardvalue = boardvalue - tables[movingpiece - 1][mov.to_square]

        # update material
        if mov.drop != None:
            if side:
                boardvalue = boardvalue + piecevalues[mov.drop - 1]
            else:
                boardvalue = boardvalue - piecevalues[mov.drop - 1]

        # update promotion
        if mov.promotion != None:
            if side:
                boardvalue = (
                    boardvalue
                    + piecevalues[mov.promotion - 1]
                    - piecevalues[movingpiece - 1]
                )
                boardvalue = (
                    boardvalue
                    - tables[movingpiece - 1][mov.to_square]
                    + tables[mov.promotion - 1][mov.to_square]
                )
            else:
                boardvalue = (
                    boardvalue
                    - piecevalues[mov.promotion - 1]
                    + piecevalues[movingpiece - 1]
                )
                boardvalue = (
                    boardvalue
                    + tables[movingpiece - 1][mov.to_square]
                    - tables[mov.promotion - 1][mov.to_square]
                )

        return mov


def make_move(mov: chess.Move, board: chess.Board):
    update_eval(board, mov, board.turn)
    board.push(mov)

    return mov


def unmake_move(board: chess.Board):
    mov = board.pop()
    update_eval(board, mov, not board.turn)

    return mov


def quiesce(board: chess.Board, alpha: int, beta: int):
    stand_pat = evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            make_move(move, board)
            score = -quiesce(board, -beta, -alpha)
            unmake_move(board)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def alphabeta(board: chess.Board, alpha: int, beta: int, depthleft: int):
    bestscore = -9999
    if depthleft == 0:
        return quiesce(board, alpha, beta)
    for move in board.legal_moves:
        make_move(move, board)
        score = -alphabeta(board, -beta, -alpha, depthleft - 1)
        unmake_move(board)
        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
        if score > alpha:
            alpha = score
    return bestscore


import chess.polyglot


def get_informed_move(board: chess.Board, depth: int):
    try:
        move = (
            chess.polyglot.MemoryMappedReader("assets/books/human.bin")
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
            make_move(move, board)
            boardValue = -alphabeta(board, -beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            unmake_move(board)
        movehistory.append(bestMove)
        return bestMove
