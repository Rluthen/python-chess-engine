from helpers import *
from psqt import *

# External
import chess


gamephase_inc = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 1,
    chess.ROOK: 2,
    chess.QUEEN: 4,
    chess.KING: 0,
}


class Evaluation:
    @staticmethod
    def eval_side(board: chess.Board, color: chess.Color) -> int:
        occupied = board.occupied_co[color]

        eg, mg = 0, 0
        game_phase = 0

        # loop over all set bits
        while occupied:
            # find the least significant bit
            square = lsb(occupied)

            piece = board.piece_type_at(square)
            if piece == None:
                continue

            # add piece values
            if color == chess.WHITE:
                eg += eg_psqt_values[piece][square]  # type: ignore
                mg += mg_psqt_values[piece][square]  # type: ignore
            else:
                eg += list(reversed(eg_psqt_values[piece]))[square]  # type: ignore
                mg += list(reversed(mg_psqt_values[piece]))[square]  # type: ignore

            game_phase += gamephase_inc[piece]  # type: ignore

            # remove lsb
            occupied = poplsb(occupied)

        # get phase factors
        mg_phase = min(game_phase, 24)
        eg_phase = 24 - mg_phase

        # return scores with phase factors
        return int((mg * mg_phase + eg * eg_phase) / 24)

    @staticmethod
    def evaluate(board: chess.Board) -> int:
        return Evaluation.eval_side(board, chess.WHITE) - Evaluation.eval_side(
            board, chess.BLACK
        )
