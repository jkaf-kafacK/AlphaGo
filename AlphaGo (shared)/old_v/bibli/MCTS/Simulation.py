from . import VERBOSE
import random

def simulate(node):
    '''
        Given a state node this function will do random playout to determine a winner 
    '''
    if VERBOSE: print('Simulation on :')
    node.print('simulate-node', VERBOSE)

    state = node.state
    
    while not state.is_terminal():
        moves = state.legal_moves()
        move = random.choice(moves)
        state = state.resulting_state(move)
    winner = state.determine_winner()
    return winner
