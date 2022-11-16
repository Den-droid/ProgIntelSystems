import chess
import chess.pgn
import chess.engine
import random
import time
from math import log, sqrt, e, inf


class node():
    def __init__(self):
        self.state = chess.Board()
        self.action = ''
        self.children = set()
        self.parent = None
        self.N = 0  # Total number of rollouts run by parent
        self.n = 0  # Number of rollouts ager this move
        self.v = 0  # result(win, draw, lose) 


def ucb1(curr_node):
    ans = curr_node.v+2 * \
        (sqrt(log(curr_node.N+e+(10**-6))/(curr_node.n+(10**-10))))
    return ans


def expand_and_rollout(curr_node):
    if curr_node.state.is_game_over():
        board = curr_node.state
        if board.result() == '1-0':
            return (1, curr_node)
        elif board.result() == '0-1':
            return (-1, curr_node)
        else:
            return (0.5, curr_node)

    all_moves = [curr_node.state.san(i)
                 for i in list(curr_node.state.legal_moves)]

    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push_san(i)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
    rnd_state = random.choice(list(curr_node.children))
    return expand_and_rollout(rnd_state)


def select(curr_node, white):
    if len(curr_node.children) == 0:
        return curr_node
    max_ucb = -inf
    if white:
        max_ucb = -inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if tmp > max_ucb:
                max_ucb = tmp
                sel_child = i

        return select(sel_child, 0)

    else:
        min_ucb = inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if (tmp < min_ucb):
                min_ucb = tmp
                sel_child = i
        return select(sel_child, 1)


def rollback(curr_node, reward):
    curr_node.n += 1
    curr_node.v += reward
    while curr_node.parent != None:
        curr_node.N += 1
        curr_node = curr_node.parent
    return curr_node


def mcts_pred(curr_node, over, white, iterations=10):
    if over:
        return -1
    all_moves = [curr_node.state.san(i)
                 for i in list(curr_node.state.legal_moves)]
    map_state_move = dict()

    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push_san(i)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
        map_state_move[child] = i

    while iterations > 0:
        if white:
            max_ucb = -inf
            first_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if tmp > max_ucb:
                    max_ucb = tmp
                    first_child = i

            sel_child = select(first_child, 0)
            reward, state = expand_and_rollout(sel_child)
            curr_node = rollback(state, reward)
            iterations -= 1
        else:
            min_ucb = inf
            first_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if tmp < min_ucb:
                    min_ucb = tmp
                    first_child = i

            sel_child = select(first_child, 1)
            reward, state = expand_and_rollout(sel_child)
            curr_node = rollback(state, reward)
            iterations -= 1

    if white:
        mx = -inf
        selected_move = ''
        for i in curr_node.children:
            tmp = ucb1(i)
            if tmp > mx:
                mx = tmp
                selected_move = map_state_move[i]
        return selected_move
    else:
        mn = inf
        selected_move = ''
        for i in curr_node.children:
            tmp = ucb1(i)
            if tmp < mn:
                mn = tmp
                selected_move = map_state_move[i]
        return selected_move


board = chess.Board()

white = 1
pgn = []
while not board.is_game_over(claim_draw=True):
    start = time.time()

    root = node()
    root.state = board
    result = mcts_pred(root, board.is_game_over(), white)
    print(time.time() - start)
    
    board.push_san(result)
    pgn.append(result)
    
    print(result)
    print(board)
    print()
    white ^= 1

print(" ".join(pgn))
print()
print(board.result())
