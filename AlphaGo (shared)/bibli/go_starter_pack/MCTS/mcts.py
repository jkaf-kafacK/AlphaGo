import random
from .Selection import select
from .Node import Node as nd
from .Simulation import simulate
from .Backprop import Backpagation as bp
from .Expansion import expand
from . import VERBOSE, LOG_F


class MCTS:
    def __init__(self, root_node, c1=0.2, c2=None):
        self.root = root_node
        self.c1 = c1
        self.c2 = c2
        return

    def iteration(self):
        # Selection
        current_node = self.root

        while True:
            selected = select(current_node)
            if selected :
                current_node = selected
            else:
                break
        # Expansion
        if not current_node.state.is_game_over():
            children = expand(current_node)
            for child in current_node.children: 
                # Simulation
                winner = simulate(child)
                # Backpropagation
                bp.backpropagate(child, winner, child.player)
                
        best_child = select(self.root)
        # print(best_child.uct, best_child.move)
        return best_child

    def move(self, n_iters):
        "Runs the MCTS algorithm iteration *n_iters* times to get an optimal move to play"
        assert n_iters >= 1
        for _ in range(n_iters-1):
            if VERBOSE : print(f'ITERATION{_+1}', file=LOG_F)
            self.iteration()

        if VERBOSE : print(f'ITERATION{n_iters}', file=LOG_F)
        node = self.iteration()

        if VERBOSE:
            print('MTCS move node :', file=LOG_F)
        node.print('move-node', VERBOSE)
        move = node.move
        return move
