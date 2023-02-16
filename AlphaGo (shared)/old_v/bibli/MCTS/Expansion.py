from . import  VERBOSE
from .Node import Node
import numpy as np 
# import jsonpickle as jp


def expand(node):
    if VERBOSE: print('Expansion on:')
    node.print('expand_node-node', VERBOSE)
    children = []
    indexes = []
    untried_moves = node.untried_moves
    for i, move in enumerate(node.untried_moves):
        child = Node(
            state=node.state.resulting_state(move),
            parent=node,
        )
        children.append(child)
        node.children.append(child)
        indexes.append(i)
    untried_moves = np.delete(untried_moves, indexes, axis=0)
    node.untried_moves = untried_moves
        
    return children
