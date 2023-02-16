from .Selection import uct1
from . import VERBOSE, LOG_F


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = state.legal_moves()
        self.move = state.last_move()
        self.player = state.current_player()
        self.uct = 0
        self.depth = 0
        if self.parent:
            self.depth = parent.depth + 1

    def is_leaf(self):
        return self.state.is_game_over()

    def average_reward(self):
        return self.wins / self.visits if self.visits != 0 else 0

    def print(self, context='', verbose=VERBOSE):
        if not verbose:
            return
        node_dict = {'move': self.move}
        if self.parent == None:
            print(node_dict, file=LOG_F)
        else:
            node_dict = {
                'parent': self.parent.move if self.parent else None,
                'depth': self.depth,
                'move': self.move,
                'color': self.player,
                'uct': self.uct,
                'visits': self.visits,
                'wins': self.wins
            }
            print(node_dict, file=LOG_F)
        print('', file=LOG_F)
        # schema = NodeSchema()
        # result = schema.dump(self)
        # pprint(result)

    def update_uct(self, c1=0.2, c2=None):
        if not c2:
            self.uct = uct1(self, c1)
            # if self.uct != 0 : print('updated uct',  self.uct)

        # def update_untried_moves(self, tried_indexes):
        #     np.delete(self.untried_moves, indexes, 0)
