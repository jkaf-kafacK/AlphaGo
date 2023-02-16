import sys

import random
from ..MCTS.Node import Node
from ..MCTS.mcts import MCTS
# from ..MTCS import MTCS
# from ..MTCS import Node


class Player:
    def __init__(self, name):
        self.color = 0
        self.name = name

    def play_ij(self, i, j, board):
        return board.move(self.color, i, j)

    def assign_color(self, color):
        self.color = color


class RandomPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def play(self, board):
        moves = board.legal_moves()
        i, j = random.choice(moves)
        return self.play_ij(i, j, board)


class MCTSPlayer(Player):
    def __init__(self, name, n_iters, c1=0.2, c2=None):
        super().__init__(name)
        self.n_iters = n_iters
        self.c1 = c1
        self.c2 = c2

    def play(self, board):
        root = Node(board)
        # root.print('play-root')
        mcts = MCTS(root, self.c1, self.c2)
        i, j = mcts.move(self.n_iters)
        # print(move)
        return self.play_ij(i, j, board)
