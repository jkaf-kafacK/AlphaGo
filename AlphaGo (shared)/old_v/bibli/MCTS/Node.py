from bibli import obj_print
from .Selection import uct1
from marshmallow import Schema, fields
from pprint import pprint

def serialize_numpy(arr):
    return arr.tolist()

# class NodeSchema(Schema):
#     parent = fields.Pluck("self", field_name)
#     children = fields.Nested("self", depth=1, many=True)
#     visits = fields.Integer()
#     wins = fields.Integer()
#     move = fields.Tuple((fields.Integer(), fields.Integer()))
#     player = fields.Integer()
#     uct = fields.Float()


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = state.legal_moves()
        self.move = state.last_move
        self.player = state.m_color
        self.uct = 0
        self.depth = 0
        if self.parent:
            self.depth = parent.depth + 1


    def is_leaf(self):
        return self.state.is_terminal()

    def average_reward(self):
        return self.wins / self.visits if self.visits != 0 else 0

    def print(self, context='', verbose=True):
        if not verbose: return
        node_dict = {
            'parent' : self.parent.move if self.parent else None,
            'depth' : self.depth,
            'move' : self.move,
            'color': self.player,
            'uct': self.uct,
            'visits': self.visits,
            'wins': self.wins
        }
        pprint(node_dict)
        print('')
        # schema = NodeSchema()
        # result = schema.dump(self)
        # pprint(result)
        
    def update_uct(self, c1=0.2, c2=None):
        if not c2:
            self.uct = uct1(self, c1)
            # if self.uct != 0 : print('updated uct',  self.uct)

        # def update_untried_moves(self, tried_indexes):
        #     np.delete(self.untried_moves, indexes, 0)