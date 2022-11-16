import chess
from math import inf, isnan
import chess.polyglot

b_pawn_table = [0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5, -10,  0,  0, -10, -5,  5,
                5, 10, 10, -20, -20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0]
w_pawn_table = b_pawn_table[::-1]
b_knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                  -40, -20,  0,  0,  0,  0, -20, -40,
                  -30,  0, 10, 15, 15, 10,  0, -30,
                  -30,  5, 15, 20, 20, 15,  5, -30,
                  -30,  0, 15, 20, 20, 15,  0, -30,
                  -30,  5, 10, 15, 15, 10,  5, -30,
                  -40, -20,  0,  5,  5,  0, -20, -40,
                  -50, -40, -30, -30, -30, -30, -40, -50]
w_knight_table = b_knight_table[::-1]
b_bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                  -10,  0,  0,  0,  0,  0,  0, -10,
                  -10,  0,  5, 10, 10,  5,  0, -10,
                  -10,  5,  5, 10, 10,  5,  5, -10,
                  -10,  0, 10, 10, 10, 10,  0, -10,
                  -10, 10, 10, 10, 10, 10, 10, -10,
                  -10,  5,  0,  0,  0,  0,  5, -10,
                  -20, -10, -10, -10, -10, -10, -10, -20]
w_bishop_table = b_bishop_table[::-1]
b_rook_table = [0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0]
w_rook_table = b_rook_table[::-1]
b_queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
                 -10,  0,  0,  0,  0,  0,  0, -10,
                 -10,  0,  5,  5,  5,  5,  0, -10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                 0,  0,  5,  5,  5,  5,  0, -5,
                 -10,  5,  5,  5,  5,  5,  0, -10,
                 -10,  0,  5,  0,  0,  0,  0, -10,
                 -20, -10, -10, -5, -5, -10, -10, -20]
w_queen_table = b_queen_table[::-1]

def mateInXMoves(score):
    half_moves_to_mate = (-(abs(score) - 99999) // (999.99))
    if not isnan(half_moves_to_mate):
        moves_to_mate = int((half_moves_to_mate - 1) // 2) + 1
        if (board.turn and score > 0) or (not board.turn and score < 0):
            side_mated = 'white'
        else:
            side_mated = 'black'
        score = 'Mate in {} for {}'.format(str(moves_to_mate), side_mated)
    return score


def qSearch(board, alpha, beta, color, starting_depth, depth=0, max_depth=4):
    if board.is_checkmate():
        return color * (1 - (0.01*(starting_depth + depth))) * -99999 if board.turn else color * (1 - (0.01*(starting_depth + depth))) * 99999
    value = color * evaluateBoard(board)
    if value >= beta:
        return beta
    if alpha < value:
        alpha = value
    if depth < max_depth:
        captureMoves = (move for move in board.generate_legal_moves() if (
            board.is_capture(move) or board.is_check()))
        for move in captureMoves:
            board.push(move)
            score = -qSearch(board, -beta, -alpha, -
                             color, depth + 1, max_depth)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def evaluateBoard(board):
    evaluation = 5
    pieces = board.pieces

    white_pawns = pieces(1, True)
    black_pawns = pieces(1, False)
    white_knights = pieces(2, True)
    black_knights = pieces(2, False)
    white_bishops = pieces(3, True)
    black_bishops = pieces(3, False)
    white_rooks = pieces(4, True)
    black_rooks = pieces(4, False)
    white_queens = pieces(5, True)
    black_queens = pieces(5, False)
    # mapping pieces to piece-square tables
    evaluation += sum(map(lambda x: w_pawn_table[x], white_pawns)) - sum(
        map(lambda x: b_pawn_table[x], black_pawns))
    evaluation += sum(map(lambda x: w_knight_table[x], white_knights)) - sum(
        map(lambda x: b_knight_table[x], black_knights))
    evaluation += sum(map(lambda x: w_bishop_table[x], white_bishops)) - sum(
        map(lambda x: b_bishop_table[x], black_bishops))
    evaluation += sum(map(lambda x: w_rook_table[x], white_rooks)) - sum(
        map(lambda x: b_rook_table[x], black_rooks))
    evaluation += sum(map(lambda x: w_queen_table[x], white_queens)) - sum(
        map(lambda x: b_queen_table[x], black_queens))
    # calculating material advantage
    evaluation += 100*(len(white_pawns) - len(black_pawns)) + 310*(len(white_knights) - len(black_knights)) + 320*(len(
        white_bishops) - len(black_bishops)) + 500*(len(white_rooks) - len(black_rooks)) + 900*(len(white_queens) - len(black_queens))
    return evaluation


def negaMaxRoot(board, depth, alpha, beta, color, max_depth):
    value = -inf
    moves = board.generate_legal_moves()
    best_move = next(moves)
    for move in moves:
        board.push(move)
        board_value = -negaMax(board, depth - 1, -
                               beta, -alpha, -color, max_depth)
        board.pop()
        if board_value > value:
            value = board_value
            best_move = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return best_move, value


def negaMax(board, depth, alpha, beta, color, max_depth):
    if board.is_fivefold_repetition() or board.is_stalemate() or board.is_seventyfive_moves():
        return 0
    if board.is_checkmate():
        return color * (1 - (0.01*(max_depth - depth))) * -99999 if board.turn else color * (1 - (0.01*(max_depth - depth))) * 99999
    if depth == 0:
        if board.is_capture(board.peek()) or board.is_check():
            return qSearch(board, alpha, beta, color, max_depth)
        return color * evaluateBoard(board)
    value = -inf
    moves = board.generate_legal_moves()
    for move in moves:
        board.push(move)
        value = max(value, -negaMax(board, depth -
                    1, -beta, -alpha, -color, max_depth))
        board.pop()
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value


def pvsRoot(board, depth, alpha, beta, color, max_depth):
    value = -inf
    moves = board.generate_legal_moves()
    bestMove = next(moves)
    for move in moves:
        board.push(move)
        board_value = -pvs(board, depth - 1, -beta, -alpha, -color, max_depth)
        board.pop()
        if board_value > value:
            value = board_value
            bestMove = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return bestMove, value


def pvs(board, depth, alpha, beta, color, max_depth):
    if board.is_fivefold_repetition() or board.is_stalemate() or board.is_seventyfive_moves():
        return 0
    if board.is_checkmate():
        return color * (1 - (0.01*(max_depth - depth))) * -99999 if board.turn else color * (1 - (0.01*(max_depth - depth))) * 99999
    if depth == 0:
        if board.is_capture(board.peek()) or board.is_check():
            return qSearch(board, alpha, beta, color, max_depth)
        return color * evaluateBoard(board)
    value = -inf
    b_search_pv = True
    moves = board.generate_legal_moves()
    for move in moves:
        board.push(move)
        if b_search_pv:
            value = -pvs(board, depth - 1, -beta, -alpha, -color, max_depth)
        else:
            value = -pvs(board, depth - 1, -alpha - 1, -alpha, -color, max_depth)
            if value > alpha and value < beta:
                value = -pvs(board, depth - 1, -beta, -alpha, -color, max_depth)
        board.pop()
        if value >= beta:
            return beta
        if value > alpha:
            alpha = value
        b_search_pv = False
    return alpha


def negaScoutRoot(board, depth, alpha, beta, color, max_depth):
    value = -inf
    moves = board.generate_legal_moves()
    best_move = next(moves)
    for move in moves:
        board.push(move)
        board_value = -negaScout(board, depth - 1, -
                                 beta, -alpha, -color, max_depth)
        board.pop()
        if board_value > value:
            value = board_value
            best_move = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return best_move, value


def negaScout(board, depth, alpha, beta, color, max_depth):
    if board.is_fivefold_repetition() or board.is_stalemate() or board.is_seventyfive_moves():
        return 0
    if board.is_checkmate():
        return color * (1 - (0.01*(max_depth - depth))) * -99999 if board.turn else color * (1 - (0.01*(max_depth - depth))) * 99999
    if depth == 0:
        if board.is_capture(board.peek()) or board.is_check():
            return qSearch(board, alpha, beta, color, max_depth)
        return color * evaluateBoard(board)
    value = -inf
    orig_beta = beta
    moves = board.generate_legal_moves()
    for move in moves:
        board.push(move)
        current = -negaScout(board, depth - 1, -
                             orig_beta, -alpha, -color, max_depth)
        if current > value:
            if orig_beta == beta or depth <= 2:
                value = current
            else:
                value = -negaScout(board, depth - 1, -
                                   beta, -current, -color, max_depth)
        if value > alpha:
            alpha = value
        board.pop()
        if alpha >= beta:
            break
        orig_beta = alpha + 1
    return value

# computer move function
def move(board, depth, color):
    bestMove, value = negaMaxRoot(
                board, depth, -inf, inf, color, depth)
    # bestMove, value = negaScoutRoot(
    #             board, depth, -inf, inf, color, depth)
    # bestMove, value = pvsRoot(board, depth, -inf, inf, color, depth)
    return bestMove, value


def makeMove(color_to_play, player_color, depth):
    if color_to_play == (player_color == 'w'):
        user_input = input(
            'Make Move (or type e to export the FEN of the position): ')
        if user_input.lower() == 'e':
            print(board.fen())
        board.push_uci(user_input)
    else:
        if color_to_play:
            computer_move, score = move(board, depth, 1)
        else:
            computer_move, score = move(board, depth, -1)
        print('best move is ' + str(computer_move))
        if score > 50000 or score < -50000:
            score = mateInXMoves(score)
        print('Position advantage is calclulated as: ' + str(score))
        board.push(computer_move)

# play against the computer
def play(fen=''):
    global board
    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()
    player_color = input('play as (w)hite or (b)lack? ')[0].lower()
    printBoard(board, player_color)
    depth = int(
        input('Difficulty Level (Search Depth) (Don\'t go over 5 yet): '))
    while not board.is_game_over():
        try:
            makeMove(board.turn, player_color, depth)
        except ValueError:
            continue
        printBoard(board, player_color)
    print('Game Over! Result: {}'.format(board.result()))

# print the board (reversed if playing as black)
def printBoard(board, player_color):
    if player_color == 'w' or player_color == True:
        print(board)
    else:
        print(str(board)[::-1])

play()